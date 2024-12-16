@echo off

:: Welcome Message
echo Welcome to Telegram Sentinel - Team Optimizers

:: Check if Python is Installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed on your system.
    echo Please install Python from https://www.python.org/ before proceeding.
    pause
    exit /b
)

python setup_config.py

echo Setup Successful
echo.
python Tele_Bot.py
echo Bot Execution Successful!
pause