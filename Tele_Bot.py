import csv
from telethon import TelegramClient, functions, types
from sentence_transformers import SentenceTransformer, util
from textblob import TextBlob
from datetime import datetime
from pytz import utc
import configparser
from fuzzywuzzy import fuzz

config = configparser.ConfigParser()
config.read('config.ini')

API_ID = config['telegram_api']['api_id']
API_HASH = config['telegram_api']['api_hash']

client = TelegramClient('crypto_scanner', API_ID, API_HASH)
nlp_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

SCAM_KEYWORDS = [
    "guaranteed profit", "100% return", "double your money",
    "investment opportunity", "no risk", "get rich quick", "limited time offer"
]

def is_keyword_match(message_text, keywords, threshold=85):
    for keyword in keywords:
        if fuzz.partial_ratio(message_text.lower(), keyword.lower()) >= threshold:
            return True
    return False


import os

def save_to_csv(flagged_data, file_path="flagged_messages.csv"):
    headers = ["Channel ID", "Channel Title", "Message Link", "Message ID", "Sender ID", "Credibility Score", "Engagement Score"]

    file_exists = os.path.isfile(file_path) 
    with open(file_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        
        if not file_exists: 
            writer.writerow(headers)
        
        writer.writerows(flagged_data)


def load_processed_channels(file_path="processed_channels.txt"):
    try:
        with open(file_path, "r") as file:
            return set(line.strip() for line in file.readlines())
    except FileNotFoundError:
        return set()

def save_processed_channel(channel_id, file_path="processed_channels.txt"):
    with open(file_path, "a") as file:
        file.write(f"{channel_id}\n")

async def fetch_and_analyze_messages(channel):
    print(f"Analyzing channel: {channel.title} ({channel.id})")
    flagged_messages = []
    active_users = set()
    flagged_count = 0
    total_messages = 0  

    try:
        now = datetime.now(utc)  
        async for message in client.iter_messages(channel, limit=100):
            if not message or not message.message:
                continue

            
            if (now - message.date).days > 30:
                continue

            total_messages += 1  

            
            keyword_flag = is_keyword_match(message.message, SCAM_KEYWORDS)

            
            sentiment_flag = TextBlob(message.message).sentiment.polarity < -0.1

            
            suspicious_phrases = [
                "guaranteed profit", "double your money", "investment opportunity",
                "100% return", "no risk", "get rich quick", "limited time offer"
            ]
            similarity_flag = any(
                util.cos_sim(nlp_model.encode(message.message), nlp_model.encode(phrase)).item() > 0.8
                for phrase in suspicious_phrases
            )

            if keyword_flag or sentiment_flag or similarity_flag:
                reason = (
                    "Keyword match" if keyword_flag else
                    "Negative sentiment" if sentiment_flag else
                    "Cosine similarity match"
                )

                
                if channel.username:
                    message_link = f"https://t.me/{channel.username}/{message.id}"
                else:
                    message_link = f"https://t.me/c/{channel.id}/{message.id}"

                flagged_messages.append([channel.id, channel.title, message_link, message.id, message.sender_id])
                flagged_count += 1

            if message.sender_id:
                active_users.add(message.sender_id)

        
        if total_messages > 0:
            scam_ratio = flagged_count / total_messages  
            credibility_score = round((1 - scam_ratio) * 100, 2)  
        else:
            credibility_score = 100  

        total_members = getattr(await client.get_entity(channel), 'participants_count', 0)
        engagement_score = round((len(active_users) / total_members) * 100, 2) if total_members else 0

        for flagged in flagged_messages:
            flagged.extend([credibility_score, engagement_score])

        
        if flagged_messages:
            save_to_csv(flagged_messages)

        print(f"Channel Credibility: {credibility_score}%, Engagement: {engagement_score}%")
        return flagged_messages

    except Exception as e:
        print(f"Error analyzing channel {channel.id}: {e}")
        return []

async def search_and_analyze_channels():
    base_search_terms = ["crypto", "bitcoin", "investment", "profit", "trading"]
    processed_channels = load_processed_channels()
    flagged_data = []
    max_channels_to_check = 50
    total_checked = 0
    iterations = 0

    while True:
        print(f"Starting iteration {iterations + 1} for new channel search.")
        new_channels_found = False

        for term in base_search_terms:
            print(f"Searching for channels with term: {term}")
            try:
                results = await client(functions.contacts.SearchRequest(
                    q=term,
                    limit=10
                ))
                channels = [chat for chat in results.chats if isinstance(chat, types.Channel)]

                
                new_channels = [channel for channel in channels if str(channel.id) not in processed_channels]

                if not new_channels:
                    print(f"No unprocessed channels found for term '{term}'.")
                    continue

                new_channels_found = True  

                
                for channel in new_channels:
                    flagged_messages = await fetch_and_analyze_messages(channel)
                    flagged_data.extend(flagged_messages)

                    
                    save_processed_channel(channel.id)
                    processed_channels.add(str(channel.id))  
                    total_checked += 1

                    if total_checked >= max_channels_to_check:
                        print("Reached the maximum number of channels to check.")
                        break

                if total_checked >= max_channels_to_check:
                    break

            except Exception as e:
                print(f"Error fetching channels for term '{term}': {e}")

        
        if not new_channels_found:
            print("No new channels found in this iteration. Retrying with broadened search terms...")
            
            base_search_terms = [f"{term} {i}" for term in base_search_terms for i in range(1, 3)]
            iterations += 1
            if iterations > 5:  
                print("No new channels found after multiple iterations. Exiting.")
                break

    print("Analysis complete. Results saved to flagged_messages.csv.")


with client:
    client.loop.run_until_complete(search_and_analyze_channels())
