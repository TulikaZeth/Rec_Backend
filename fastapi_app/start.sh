#!/bin/bash
# Startup script for local development

echo "Starting Recruitment Portal Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the application
echo "Starting FastAPI application..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
