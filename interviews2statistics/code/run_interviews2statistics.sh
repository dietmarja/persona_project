#!/bin/bash

# Navigate to the directory containing the script
cd "$(dirname "$0")"

# Run the main Python script
python3 interviews2statistics.py


# Pause to keep the terminal window open (useful if double-clicking the script)
read -p "Press enter to continue"