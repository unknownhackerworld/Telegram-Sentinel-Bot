@echo off

:: Welcome Message
echo Welcome to Telegram Sentinel - Team Optimizers
echo Please Replace your API and HASH key from my.telegram.org in config.ini
echo Thank You
echo Press Any Key to Install Required Packages
pause

:: Check if Python is Installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed on your system.
    echo Please install Python from https://www.python.org/ before proceeding.
    pause
    exit /b
)

python setup_config.py
pip install -r requirements.txt

python Tele_Bot.py
echo Bot Execution Successful!
pause