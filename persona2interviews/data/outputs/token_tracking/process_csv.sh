#!/bin/bash

# Input file
input_file="token_distribution_persona_pool100.csv"

# Temporary file to store the processed data
temp_file="temp_token_distribution_persona_pool100.csv"

# Remove lines that start with "combined" and ensure each line is unique
grep -v '^combined' "$input_file" | sort -u > "$temp_file"

# Overwrite the original file with the processed data
mv "$temp_file" "$input_file"

echo "File processed successfully."

