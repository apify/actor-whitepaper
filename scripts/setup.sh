#!/bin/bash

echo "󰋼  Setting up development environment..."

# Create virtual environment if it doesn't exist.
if [ ! -d ".venv" ]; then
    echo -e "\n󰋼  Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment.
echo -e "\n󰋼  Activating virtual environment..."
source .venv/bin/activate || source .venv/Scripts/activate

# Install/upgrade pip and dependencies.
echo -e "\n󰋼  Installing Python dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Make scripts executable.
echo -e "\n󰋼  Making scripts executable..."
chmod +x scripts/*.sh

echo -e "\n󰋼  Setup complete! Activate the virtual environment with:"
echo "source .venv/bin/activate # Unix/Mac"
echo ".venv\\Scripts\\activate # Windows"
