#!/bin/bash

# Directory containing the files (you can change this to the desired directory)
directory="."

# Loop through all files in the directory
for file in "$directory"/*; do
    # Check if the file name contains the prefix "group1_"
    if [[ "$(basename "$file")" == group1_* ]]; then
        # Extract the new filename by removing the prefix "group1_"
        new_filename=$(basename "$file" | sed 's/^group1_//')
        # Rename the file
        mv "$file" "$directory/$new_filename"
        echo "Renamed $file to $directory/$new_filename"
    fi
done
