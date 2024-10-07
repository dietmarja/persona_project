#!/bin/bash

# Navigate to the project root directory
cd "$(dirname "$0")/.."

# Set the Python path to include the project root and the 'code' directory
export PYTHONPATH="$PYTHONPATH:$(pwd):$(pwd)/code"

# Run the focus group simulator
python "$(pwd)/code/persona2interviews.py"
