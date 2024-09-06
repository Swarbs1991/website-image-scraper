#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 not found. Please install Python 3 from https://www.python.org/downloads/"
    exit
fi

# Install pip if not installed
if ! command -v pip &> /dev/null
then
    echo "Installing pip..."
    python3 -m ensurepip --upgrade
fi

# Install the required libraries
pip install -r requirements.txt

echo "Dependencies installed successfully!"
