# File: code/sub/persona_selector.py

import csv
import random
import os

def load_persona_pool(file_path):
    print(f"Attempting to load persona pool from: {file_path}")
    absolute_path = os.path.abspath(file_path)
    print(f"Absolute path: {absolute_path}")
    if not os.path.exists(absolute_path):
        raise FileNotFoundError(f"Persona pool file not found: {absolute_path}")
    with open(absolute_path, 'r') as f:
        # Read the first line to get the headers
        headers = next(f).strip().split(';')
        headers = [header.strip() for header in headers]
        
        reader = csv.reader(f, delimiter=';')
        pool = []
        for row in reader:
            if len(row) == len(headers):
                persona = {headers[i].strip(): value.strip() for i, value in enumerate(row)}
                pool.append(persona)
            else:
                print(f"Skipping malformed row: {row}")
        
        if pool:
            print(f"Columns found in CSV: {', '.join(headers)}")
            print("First persona in pool:", pool[0])
        else:
            print("Warning: No data found in the persona pool file.")
    print(f"Loaded {len(pool)} personas from the pool")
    return pool



def get_case_insensitive(dict_obj, key):
    key_lower = key.lower()
    for k in dict_obj.keys():
        if k.lower() == key_lower:
            return dict_obj[k]
    raise KeyError(f"No case-insensitive match for '{key}' found in {list(dict_obj.keys())}")

def select_personas(persona_pool, criteria_list):
    selected_personas = []
    for criteria in criteria_list:
        print(f"Selecting personas for criteria: {criteria}")
        matching_personas = []
        for p in persona_pool:
            try:
                role_match = p['Role'].lower() == criteria['role'].lower()
                background_match = p['Background'].lower() == criteria['background'].lower()
                gender_match = p['Gender'].lower() == criteria['gender'].lower()
                
                if role_match and background_match and gender_match:
                    matching_personas.append(p)
                else:
                    print(f"No match for persona: {p}")
                    print(f"Role match: {role_match}, Background match: {background_match}, Gender match: {gender_match}")
            except KeyError as e:
                print(f"KeyError for persona: {p}")
                print(f"Error: {e}")

        print(f"Found {len(matching_personas)} matching personas")
        if len(matching_personas) < criteria['count']:
            raise ValueError(f"Not enough personas matching criteria: {criteria}. Found {len(matching_personas)}.")
        selected = random.sample(matching_personas, criteria['count'])
        selected_personas.extend(selected)
        print(f"Selected {len(selected)} personas")
    return selected_personas


def get_personas(config):
    print("Getting personas from config:", config['focus_group'])
    
    persona_pool_file = config['focus_group'].get('persona_pool_file')
    if not persona_pool_file:
        raise ValueError("persona_pool_file not specified in the configuration")
    
    print(f"Using persona pool file: {persona_pool_file}")
    
    try:
        persona_pool = load_persona_pool(persona_pool_file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please make sure the persona_pool_file is correctly specified in your config and the file exists.")
        raise
    
    if 'personas' not in config['focus_group']:
        raise KeyError("'personas' key not found in focus_group configuration")
    
    return select_personas(persona_pool, config['focus_group']['personas'])

# Add this line at the end of the file for debugging
print("persona_selector module loaded")