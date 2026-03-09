#!/bin/bash

# Start PlantCare AI Frontend Server

cd "$(dirname "$0")/plantcare-ai/frontend"

echo "🌐 Starting PlantCare AI Frontend..."
echo "Open http://localhost:5500 in your browser"
python3 -m http.server 5500
