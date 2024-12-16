import configparser
import os

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

def setup_config():
    config = configparser.ConfigParser()

    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        if is_valid_config(config):
            print("\nValid API details found in config.ini. Proceeding...")
            return  
        else:
            print("\nInvalid API details found in config.ini. Reconfiguring... Open https://my.telegram.org/ for API and HASH of Your Telgram Account")

    api_id, api_hash = get_user_input()
    save_config(api_id, api_hash)

if __name__ == "__main__":
    setup_config()
