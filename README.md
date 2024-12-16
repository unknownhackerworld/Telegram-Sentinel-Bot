# Telegram Sentinel - Team Optimizers

Welcome to Telegram Sentinel, a project by Team Optimizers. This guide explains the steps to set up and run the project.

## Prerequisites

Ensure that your system meets the following requirements:

- Python 3.6 or higher is installed.
- `pip` (Python package manager) is installed.
- A valid Telegram API ID and API Hash from [my.telegram.org](https://my.telegram.org/).

## Setup Instructions

### Method 1: Download via Google Drive

   - Access the project files from the following Google Drive link: [Telegram Sentinel Project Files](https://drive.google.com/drive/folders/1qd0qX_hXBsvZaxcFGcdzMzuZo4x_Joaj?usp=drive_link).
   - Download and extract the files to your desired location.

### Method 2: Clone from GitHub

   - Clone the repository using the following command:

     ```bash
     git clone https://github.com/unknownhackerworld/Telegram-Sentinel-Bot.git
     cd Telegram-Sentinel-Bot
     ```

2. **Run the Setup Script**

   Use the provided `start.bat` file to set up and run the project.

   - Navigate to the project directory and double-click `start.bat`.
   - The script will:
     - Check if Python is installed.
     - Run `setup_config.py` to validate or configure your `config.ini` file.
     - Install required Python dependencies using `pip`.
     - Launch the `Tele_Bot.py` script.

3. **Using `setup_config.py`**

   - The `setup_config.py` script ensures that the `config.ini` file is properly configured.
   - If valid API credentials are not found, the script will prompt you to enter your Telegram API ID and API Hash.
   - These details will be saved to `config.ini` for future use.

4. **Install Dependencies Manually (Optional)**

   If you prefer to install dependencies manually, run the following command:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Bot Manually (Optional)**

   After installing dependencies, you can manually start the bot with:

   ```bash
   python Tele_Bot.py
   ```

## Troubleshooting

- **Python Not Found**:
  If the script reports that Python is not installed, download and install Python from [python.org](https://www.python.org/).

- **Invalid API or Hash**:
  Ensure that you have entered valid credentials in `config.ini`. Use the `setup_config.py` script to reconfigure if needed.

- **Dependency Errors**:
  Ensure you have a stable internet connection to install the dependencies.

## Contact

- **Name**: Allen Joseph G
- **Email**: rlearning6@gmail.com
