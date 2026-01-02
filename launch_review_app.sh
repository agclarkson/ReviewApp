#!/bin/bash

echo "========================================"
echo "ORRA Referee Review System"
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3 from https://www.python.org/downloads/"
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if openpyxl is installed
python3 -c "import openpyxl" &> /dev/null
if [ $? -ne 0 ]; then
    echo "Installing required library..."
    pip3 install openpyxl
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install openpyxl"
        echo "Please run: pip3 install openpyxl"
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

echo "Starting Referee Review System..."
echo ""
python3 referee_review_app.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Application failed to start"
    read -p "Press Enter to exit..."
fi
