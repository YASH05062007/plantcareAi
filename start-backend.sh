#!/bin/bash

# Start PlantCare AI Backend Server

cd "$(dirname "$0")/plantcare-ai/backend"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Run setup.sh first."
    exit 1
fi

echo "🚀 Starting PlantCare AI Backend..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000
