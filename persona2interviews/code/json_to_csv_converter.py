import json
import csv
import os

def convert_json_to_csv(json_file, csv_file):
    # Read JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Prepare CSV header
    header = ['Persona'] + [f'Q{q}{o}' for q in range(1, 6) for o in 'ABCD']

    # Prepare CSV rows
    rows = []
    for i, person in enumerate(data, 1):
        row = [f'P{i}']
        for question in person['responses']:
            responses = question['response'].split(',')
            for option in 'ABCD':
                row.append('1' if option in responses else '0')
        rows.append(row)

    # Write CSV file
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"CSV file created: {csv_file}")

# Usage
json_file = 'data/outputs/simulation_results.json'
csv_file = 'data/outputs/simulation_results.csv'

# Ensure the output directory exists
os.makedirs(os.path.dirname(csv_file), exist_ok=True)

# Convert JSON to CSV
convert_json_to_csv(json_file, csv_file)
