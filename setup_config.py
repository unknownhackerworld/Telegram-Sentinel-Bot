import configparser
import os
import sys
import asyncio  

CONFIG_FILE = 'config.ini'

def is_valid_config(config):
    try:
        api_id = int(config['telegram_api']['api_id'])
        api_hash = config['telegram_api']['api_hash']
        return api_id > 0 and len(api_hash) > 0
    except (KeyError, ValueError):
        return False

def get_user_input():
    print("Enter your Telegram API credentials.")
    api_id = input("API ID (numeric): ").strip()
    while not api_id.isdigit():
        print("API ID must be a numeric value.")
        api_id = input("API ID (numeric): ").strip()

    api_hash = input("API Hash: ").strip()
    while not api_hash:
        print("API Hash cannot be empty.")
        api_hash = input("API Hash: ").strip()

    return api_id, api_hash

def save_config(api_id, api_hash):
    config = configparser.ConfigParser()
    config['telegram_api'] = {
        'api_id': api_id,
        'api_hash': api_hash
    }
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
    print("\nAPI details saved to config.ini successfully!")

async def verify_client(api_id, api_hash):
    from telethon import TelegramClient
    print("Please Enter Mobile Number With Country Code (+91) if asked")
    client = TelegramClient('crypto_scanner', api_id, api_hash)
    await client.start()  

    if await client.is_user_authorized():
        print("Client is authorized!")
    else:
        print("Authorization required. Please follow the prompts.")

    await client.disconnect()

def setup_config():
    config = configparser.ConfigParser()

    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        if is_valid_config(config):
            print("\nValid API details found in config.ini. Proceeding...")
        else:
            print("\nInvalid API details found in config.ini. Reconfiguring...\nOpen https://my.telegram.org/ for API and HASH of Your Telegram Account")
            api_id, api_hash = get_user_input()
            save_config(api_id, api_hash)

    try:
        
        import csv
        from telethon import TelegramClient, functions, types
        from sentence_transformers import SentenceTransformer, util
        from textblob import TextBlob
        from datetime import datetime
        from pytz import utc
        from fuzzywuzzy import fuzz

        print("All required packages are already installed.")

    except Exception as e:
        
        print(f"Error: {e}")
        print("Some packages are missing. Attempting to install missing packages...")
        os.system("pip install -r requirements.txt")

    finally:
        print("Setup process completed. Verifying package installation...")

        try:
            api_id = int(config['telegram_api']['api_id'])
            api_hash = config['telegram_api']['api_hash']
            asyncio.run(verify_client(api_id, api_hash))  

        except Exception as e:
            print(f"Error during client setup: {e}")
            sys.exit(1)

if __name__ == "__main__":
    setup_config()
