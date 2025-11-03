#!/bin/bash
# Simple Pacman Game Launcher for Mac

echo "Starting Simple Pacman Game..."
echo "Use WASD or Arrow Keys to move, ESC to quit"
echo ""

# Change to the game directory
cd "$(dirname "$0")"

# Run the game using the virtual environment Python
./.venv/bin/python pacman.py