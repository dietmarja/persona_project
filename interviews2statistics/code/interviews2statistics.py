# File: code/interviews2statistics.py

import csv
import logging
import os
import sys
import yaml
import pandas as pd
import re
from datetime import datetime
from typing import List, Tuple

from sub.file_processing import read_interviews_from_directory
from sub.analysis1 import analyze_interview
from sub.analysis2 import perform_statistical_analysis
from sub.barchart import generate_charts, generate_tech_score_chart
from sub.idea_buildup import calculate_idea_buildup
from sub.classes import Contribution
from sub.barchart import generate_tech_score_chart



def save_rankings(config, tech_ranking, tfidf_ranking, idea_buildup_ranking, maverick_probability, maverick_list):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"i2s_rankings_{timestamp}.txt"
    output_file = os.path.join(config['output']['stat_results_directory'], filename)

    print("\nDebugging information:")
    print("Tech ranking:")
    print(tech_ranking)
    print("\nTech ranking columns:", tech_ranking.columns)

    print("\nIdea buildup ranking:")
    print(idea_buildup_ranking)
    print("\nIdea buildup ranking columns:", idea_buildup_ranking.columns)

    with open(output_file, 'w') as f:
        f.write("I2S Rankings\n\n")
        f.write("Tech Score Ranking:\n")
        f.write(tech_ranking[['filename', 'tech_score_mean', 'Tech_Rank']].to_string(index=False))
        f.write("\n\nMaverick Information:\n")
        f.write(f"Maverick Interjection Probability: {maverick_probability}\n")
        f.write("Maverick Personas:\n")
        for persona in maverick_list:
            f.write(f"- {persona}\n")
        if tfidf_ranking is not None:
            f.write("\n\nTFIDF Ranking:\n")
            f.write(tfidf_ranking[['filename', 'TFIDF', 'TFIDF_Rank']].to_string(index=False))
        f.write("\n\nIdea Build-up Ranking:\n")
        f.write(idea_buildup_ranking[['filename', 'idea_buildup_score_mean', 'Idea_Buildup_Rank']].to_string(index=False))

    print(f"\nI2S Rankings saved to {output_file}")

def get_next_batch_number(config):
    batch_file = os.path.join(config['output']['stat_results_directory'], 'batch_number.txt')
    if os.path.exists(batch_file):
        with open(batch_file, 'r') as f:
            batch_number = int(f.read().strip())
        batch_number += 1
    else:
        batch_number = 1

    with open(batch_file, 'w') as f:
        f.write(str(batch_number))

    return batch_number



def load_maverick_config(config_path):
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        # Check if 'maverick' key exists
        if 'maverick' in config:
            # Check if 'interjection_probability' exists under 'maverick'
            if 'interjection_probability' in config['maverick']:
                return config['maverick']['interjection_probability']
            else:
                logging.warning("'interjection_probability' not found in maverick config. Using default value of 0.")
        else:
            logging.warning("'maverick' key not found in config. Using default value of 0.")
        
        # Return a default value if the key is not found
        return 0
    except FileNotFoundError:
        logging.error(f"Maverick config file not found: {config_path}")
        return 0
    except yaml.YAMLError as e:
        logging.error(f"Error parsing maverick config file: {e}")
        return 0



def load_persona_pool(file_path):
    try:
        print(f"Attempting to load persona pool from: {file_path}")
        df = pd.read_csv(file_path)
        print(f"File loaded successfully. Shape: {df.shape}")
        print(f"Columns: {', '.join(df.columns)}")

        # Check if 'role' column exists
        if 'role' not in df.columns:
            print(f"Error: 'role' column not found in {file_path}")
            return []

        # The expert/persona name is in the 'expert' column
        if 'expert' not in df.columns:
            print(f"Error: 'expert' column not found in {file_path}")
            return []

        # Strip whitespace from 'role' column
        df['role'] = df['role'].str.strip()

        print("Searching for mavericks...")
        mavericks = df[df['role'].str.lower() == 'maverick']['expert'].tolist()

        print(f"Unique values in 'role' column: {df['role'].unique()}")

        if not mavericks:
            print("No mavericks found in the persona pool.")
        else:
            print(f"Mavericks found: {', '.join(mavericks)}")

        return mavericks
    except Exception as e:
        print(f"Error loading persona pool file: {e}")
        return []

def is_maverick(persona, maverick_list, maverick_probability):
    return maverick_probability if persona in maverick_list else 0

def update_results_csv(config, summary_stats, tech_ranking, idea_buildup_ranking, all_results, maverick_probability, maverick_list):
    csv_file_path = os.path.join(config['input']['input_directory'], config['input']['main_file'])
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    batch_number = get_next_batch_number(config)

    # Get the "no persona/plain LLM" scores from the summary stats
    no_persona_file = 'no_persona_interview.txt'
    no_persona_scores = summary_stats[summary_stats['filename'] == no_persona_file].iloc[0]

    # Function to normalize scores
    def normalize_score(score, no_persona_score):
        if pd.isna(no_persona_score) or no_persona_score == 0:
            return 0
        return (score / no_persona_score * 100) - 100

    # Prepare the new data
    new_data = []

    # Add data for each iteration
    for result in all_results:
        persona_name = os.path.splitext(result['filename'])[0]
        new_row = {
            'Batch': batch_number,
            'Date': current_date,
            'Persona': result['filename'],
            'Iteration': result['iteration'],
            'Maverick': maverick_probability if persona_name in maverick_list else 0,
            'Tech_Score': result['tech_score'],
            'Ethics_Score': result['ethics_score'],
            'Edu_Score': result['education_score'],
            'Idea_Buildup_Score': result['idea_buildup_score'],
        }
        new_data.append(new_row)

    # Add aggregated data
    for _, row in summary_stats.iterrows():
        persona_name = os.path.splitext(row['filename'])[0]
        new_row = {
            'Batch': batch_number,
            'Date': current_date,
            'Persona': row['filename'],
            'Iteration': -999,  # Indicates this is a summary row
            'Maverick': maverick_probability if persona_name in maverick_list else 0,
            'Tech_Score': row['tech_score_mean'],
            'Tech_Score_Std': row['tech_score_std'],
            'Normalized_Tech_Score': normalize_score(row['tech_score_mean'], no_persona_scores['tech_score_mean']),
            'Ethics_Score': row['ethics_score_mean'],
            'Ethics_Score_Std': row['ethics_score_std'],
            'Normalized_Ethics_Score': normalize_score(row['ethics_score_mean'], no_persona_scores['ethics_score_mean']),
            'Edu_Score': row['education_score_mean'],
            'Edu_Score_Std': row['education_score_std'],
            'Normalized_Edu_Score': normalize_score(row['education_score_mean'], no_persona_scores['education_score_mean']),
            'Idea_Buildup_Score': row['idea_buildup_score_mean'],
            'Idea_Buildup_Score_Std': row['idea_buildup_score_std'],
            'Normalized_Idea_Buildup_Score': normalize_score(row['idea_buildup_score_mean'], no_persona_scores['idea_buildup_score_mean']),
        }

        # Add rankings
        new_row['Tech_Rank'] = tech_ranking[tech_ranking['filename'] == row['filename']]['Tech_Rank'].values[0]
        new_row['Idea_Buildup_Rank'] = idea_buildup_ranking[idea_buildup_ranking['filename'] == row['filename']]['Idea_Buildup_Rank'].values[0]

        new_data.append(new_row)

    # Create DataFrame
    new_df = pd.DataFrame(new_data)

    # Check if the file exists
    if os.path.exists(csv_file_path):
        # If it exists, read the existing data
        existing_df = pd.read_csv(csv_file_path)
        # Append new data to existing data
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        # If it doesn't exist, use only the new data
        updated_df = new_df

    # Write the updated data to the CSV file
    updated_df.to_csv(csv_file_path, index=False)
    print(f"Updated results (including individual iterations) appended to {csv_file_path}")

    # Double-check the written file
    print("\nContents of the CSV file after writing:")
    with open(csv_file_path, 'r') as f:
        print(f.read())

#def extract_iterations(content: str) -> List[Tuple[int, Contribution]]:
#    iterations = []
#    pattern = r"--- Discussion Start \(Iteration (\d+)\) ---(.*?)--- Summary End \(Iteration \1\) ---"
#    matches = re.findall(pattern, content, re.DOTALL)
#
#    for iteration, text in matches:
#        iterations.append((int(iteration), Contribution(text=text.strip())))
#
#    return iterations


def extract_iterations(content: str) -> List[Tuple[int, Contribution]]:
    iterations = []
    # Updated pattern to match only the start of each iteration
    pattern = r"--- Iteration (\d+) ---\s*(.*?)(?=--- Iteration \d+ ---|$)"
    matches = re.findall(pattern, content, re.DOTALL)

    if not matches:
        logging.warning(f"No iterations found in the content. Content preview: {content[:200]}...")
        return iterations

    for iteration, text in matches:
        iterations.append((int(iteration), Contribution(text=text.strip())))

    logging.info(f"Extracted {len(iterations)} iterations from the content.")
    return iterations


def main():
    print("Starting Interviews2Statistics (I2S) analysis...")

    # Load configuration
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    input_directory = config['input']['input_directory']
    print(f"Input directory: {input_directory}")

    # Read interviews (only .txt files)
    interviews = [f for f in os.listdir(input_directory) if f.endswith('.txt')]

    if not interviews:
        print("No valid interviews found in the specified directory.")
        return

    # Read all interviews and store them
    all_interviews = {}
    for filename in interviews:
        file_path = os.path.join(input_directory, filename)
        with open(file_path, 'r') as file:
            content = file.read()
        all_interviews[filename] = extract_iterations(content)

    # Calculate max_length here, after all_interviews is populated
    max_length = max(len(contrib.text.split()) for filename, contributions in all_interviews.items() for _, contrib in contributions)
    print(f"Maximum interview length: {max_length} words")

    all_results = []
    for filename, iterations in all_interviews.items():
        print(f"Processing {filename} ...")

        print(f"Calculating idea buildup for {filename}...")
        idea_buildup_scores = [calculate_idea_buildup(iteration[1].text) for iteration in iterations]
        print("Idea buildup calculation complete.")

        results = analyze_interview(filename, iterations, config, max_length)
        for i, result in enumerate(results):
            result['idea_buildup_score'] = idea_buildup_scores[i]
        all_results.extend(results)

        print(f"Processed {len(iterations)} iterations for {filename}")

    print("\nPerforming I2S statistical analysis...")
    summary_stats, full_data, tech_ranking, tfidf_ranking, idea_buildup_ranking, correlation_matrix, anova_results, tukey_results, model_results = perform_statistical_analysis(config, all_results)

    # Load maverick configuration
    maverick_probability = load_maverick_config(config['maverick_config_path'])

    # Load maverick list from persona pool
    maverick_list = load_persona_pool(config['input']['persona_pool_file'])
    if not maverick_list:
        print("Warning: No mavericks found or error in loading persona pool.")

    # Update the interviews2statistics_results.csv file
    update_results_csv(config, summary_stats, tech_ranking, idea_buildup_ranking, all_results, maverick_probability, maverick_list)

    # Save rankings
    save_rankings(config, tech_ranking, tfidf_ranking, idea_buildup_ranking, maverick_probability, maverick_list)

    print("\nGenerating I2S charts...")
    generate_charts(config)

    print("\nColumns in full_data:")
    print(full_data.columns)

    # Identify score columns (assuming they end with '_score' or '_Score')
    score_columns = [col for col in full_data.columns if col.lower().endswith('_score')]

    if not score_columns:
        print("Warning: No score columns found. Cannot create correlation matrix.")
    else:
        print("\nIdentified score columns:")
        print(score_columns)

        # Compute and display correlation table
        correlation_matrix = full_data[score_columns].corr()

        print("\nI2S Correlation Table:")
        print(correlation_matrix.to_string())

    print("\nI2S Rankings Comparison:")
    print(tech_ranking.columns)
    print(idea_buildup_ranking.columns)


    generate_tech_score_chart(config, summary_stats)


    # Use the actual column names from tech_ranking and idea_buildup_ranking
    tech_cols = tech_ranking.columns.tolist()
    idea_cols = idea_buildup_ranking.columns.tolist()

    comparison = tech_ranking[tech_cols]
    if tfidf_ranking is not None:
        tfidf_cols = tfidf_ranking.columns.tolist()
        comparison = pd.merge(comparison, tfidf_ranking[tfidf_cols], on=tech_cols[0])
    comparison = pd.merge(comparison, idea_buildup_ranking[idea_cols], on=tech_cols[0])
    print(comparison.to_string(index=False))




    comparison = tech_ranking[tech_cols]
    if tfidf_ranking is not None:
        tfidf_cols = tfidf_ranking.columns.tolist()
        comparison = pd.merge(comparison, tfidf_ranking[tfidf_cols], on=tech_cols[0])
    comparison = pd.merge(comparison, idea_buildup_ranking[idea_cols], on=tech_cols[0])
    print(comparison.to_string(index=False))

    # Create a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create the filename
    comparison_filename = f"i2s_comparison_{timestamp}.csv"

    # Get the output directory from the config
    output_directory = config['output']['stat_results_directory']

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Create the full file path
    comparison_file_path = os.path.join(output_directory, comparison_filename)

    # Save the comparison table to a CSV file
    comparison.to_csv(comparison_file_path, index=False)

    print(f"\nComparison table saved to: {comparison_file_path}")

if __name__ == "__main__":
    main()
