@echo off
setlocal

echo ===================================================
echo     Gaming News AI Agent - Setup and Run Script
echo ===================================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your system PATH. 
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b
)

if not exist ".env" (
    echo [INFO] First time setup! Let's get your API keys.
    echo.
    echo (1/2) You can get an OpenAI API key from: https://platform.openai.com/api-keys
    set /p OPENAI_KEY="Paste your OpenAI API Key here: "
    echo.
    echo (2/2) You can create a Teams Webhook by right-clicking a Teams channel -^> Workflows -^> Create new -^> Post to a channel when a webhook request is received.
    set /p TEAMS_URL="Paste your Teams Webhook URL here: "
    
    echo OPENAI_API_KEY=%OPENAI_KEY%> .env
    echo TEAMS_WEBHOOK_URL=%TEAMS_URL%>> .env
    echo.
    echo [SUCCESS] Settings saved!
    echo.
) else (
    echo [INFO] Found existing configuration file.
)

if not exist "venv" (
    echo [INFO] Setting up the Python environment (this only happens once)...
    python -m venv venv
)

echo [INFO] Loading environment and dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt -q

echo.
echo ===================================================
echo     The Agent is running! Keep this window open.      
echo     (You can minimize it, but don't close it)
echo ===================================================
python main.py

pause
