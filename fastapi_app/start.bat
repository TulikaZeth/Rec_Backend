@echo off
REM Startup script for local development on Windows

echo Starting Recruitment Portal Backend...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Start the application
echo Starting FastAPI application...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
