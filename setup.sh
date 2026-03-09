#!/bin/bash

# PlantCare AI Setup Script

echo "🌿 Setting up PlantCare AI..."

# Check if we're in the right directory
if [ ! -d "plantcare-ai" ]; then
    echo "❌ Error: plantcare-ai directory not found"
    echo "Please run this script from the plantcareAi root directory"
    exit 1
fi

# Backend setup
echo ""
echo "📦 Installing backend dependencies..."
cd plantcare-ai/backend

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "To run the backend:"
echo "  cd plantcare-ai/backend"
echo "  source .venv/bin/activate"
echo "  uvicorn main:app --reload"
echo ""
echo "To run the frontend:"
echo "  cd plantcare-ai/frontend"
echo "  python3 -m http.server 5500"
echo ""
echo "🚀 Setup complete! Happy coding!"
