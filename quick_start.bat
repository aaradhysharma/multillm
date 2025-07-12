@echo off
echo.
echo ===============================================
echo   Multi-LLM Query Tool - Quick Setup
echo ===============================================
echo.

echo Installing Python packages...
pip install -r requirements.txt

echo.
echo Setting up environment file...
if not exist .env (
    copy env_example.txt .env
    echo .env file created from template
) else (
    echo .env file already exists
)

echo.
echo ===============================================
echo   Setup Complete!
echo ===============================================
echo.
echo Next steps:
echo 1. Edit .env file with your API keys
echo 2. Run: python main.py --setup
echo 3. Start querying: python main.py -p "Your question"
echo.
echo For help: python main.py --help
echo.
pause 