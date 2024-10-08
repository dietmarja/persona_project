# code/interviews2statistics.py

import csv
import os
import sys
import yaml
import pandas as pd
from datetime import datetime
from sub.file_processing import read_interviews_from_directory
from sub.analysis1 import analyze_interview
from sub.analysis2 import perform_statistical_analysis
from sub.barchart import generate_charts
from sub.idea_buildup import calculate_idea_buildup

def save_rankings(config, tech_ranking, tfidf_ranking, idea_buildup_ranking):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"i2s_rankings_{timestamp}.txt"
    output_file = os.path.join(config['output']['stat_results_directory'], filename)
    
    with open(output_file, 'w') as f:
        f.write("I2S Rankings\n\n")
        f.write("Tech Score Ranking:\n")
        f.write(tech_ranking[['Persona', 'Tech_Score', 'Tech_Rank']].to_string(index=False))
        if tfidf_ranking is not None:
            f.write("\n\nTFIDF Ranking:\n")
            f.write(tfidf_ranking[['Persona', 'TFIDF', 'TFIDF_Rank']].to_string(index=False))
        f.write("\n\nIdea Build-up Ranking:\n")
        f.write(idea_buildup_ranking[['Persona', 'Idea_Buildup_Score', 'Idea_Buildup_Rank']].to_string(index=False))
    
    print(f"I2S Rankings saved to {output_file}")

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
    

def is_maverick(persona):
    # Define your maverick personas here
    maverick_personas = ['ai_ethicist', 'professor_of_ai']  # Add more as needed
    return 1 if persona.lower() in maverick_personas else 0

def update_results_csv(config, summary_stats, tech_ranking, idea_buildup_ranking, all_results):
    csv_file_path = os.path.join(config['output']['stat_results_directory'], 'interviews2statistics_results.csv')
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    batch_number = get_next_batch_number(config)
    
    print("This is all_results!!!")    
    print(all_results)    

    # Prepare the new data
    new_data = []
    
    # Add rows for each iteration
    for result in all_results:
        row = {
            'Batch': batch_number,
            'Date': current_date,
            'Persona': result['filename'],
            'Iteration': result['iteration'],
            'Tech_Score': result['tech_score'],
            'Ethics_Score': result['ethics_score'],
            'Edu_Score': result['education_score'],
            'Idea_Buildup_Score': result['idea_buildup_score'],
            'Maverick': is_maverick(result['filename'])
        }
        new_data.append(row)
    
    # Add aggregated rows
    for persona in summary_stats.index:
        row = {
            'Batch': batch_number,
            'Date': current_date,
            'Persona': persona,
            'Iteration': -999,
            'Tech_Score': summary_stats.loc[persona, ('Tech_Score', 'mean')],
            'Ethics_Score': summary_stats.loc[persona, ('Ethics_Score', 'mean')],
            'Edu_Score': summary_stats.loc[persona, ('Edu_Score', 'mean')],
            'Idea_Buildup_Score': summary_stats.loc[persona, ('Idea_Buildup_Score', 'mean')],
            'Maverick': is_maverick(persona)
        }
        row['Tech_Rank'] = tech_ranking[tech_ranking['Persona'] == persona]['Tech_Rank'].values[0]
        row['Idea_Buildup_Rank'] = idea_buildup_ranking[idea_buildup_ranking['Persona'] == persona]['Idea_Buildup_Rank'].values[0]
        new_data.append(row)
    
    # Add focus group data if available
    if 'focus_group_1' in summary_stats.index:
        focus_group_row = {
            'Batch': batch_number,
            'Date': current_date,
            'Persona': 'Focus Group',
            'Iteration': -999,
            'Tech_Score': summary_stats.loc['focus_group_1', ('Tech_Score', 'mean')],
            'Tech_Rank': None,
            'Ethics_Score': summary_stats.loc['focus_group_1', ('Ethics_Score', 'mean')],
            'Edu_Score': summary_stats.loc['focus_group_1', ('Edu_Score', 'mean')],
            'Idea_Buildup_Score': summary_stats.loc['focus_group_1', ('Idea_Buildup_Score', 'mean')],
            'Idea_Buildup_Rank': None,
            'Maverick': 0
        }
        new_data.append(focus_group_row)
    
    new_df = pd.DataFrame(new_data)
    
    # Define the correct column order
    columns = ['Batch', 'Date', 'Persona', 'Iteration', 'Maverick', 'Tech_Score', 'Tech_Rank', 
               'Ethics_Score', 'Edu_Score', 'Idea_Buildup_Score', 'Idea_Buildup_Rank']
    
    # Ensure all columns are present, fill with None if missing
    for col in columns:
        if col not in new_df.columns:
            new_df[col] = None
    
    new_df = new_df[columns]  # Reorder columns
    
    # Check if file exists and append or create new file
    if os.path.exists(csv_file_path):
        existing_df = pd.read_csv(csv_file_path)
        # Ensure existing DataFrame has all necessary columns
        for col in columns:
            if col not in existing_df.columns:
                existing_df[col] = None
        existing_df = existing_df[columns]  # Reorder columns in existing DataFrame
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        updated_df = new_df
    
    # Write the updated data to the CSV file
    updated_df.to_csv(csv_file_path, index=False)
    print(f"Updated results written to {csv_file_path}")

def main():
    print("Starting Interviews2Statistics (I2S) analysis...")
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    interviews = read_interviews_from_directory(config['input']['input_directory'])
    
    if not interviews:
        print("No valid interviews found in the specified directory.")
        return

    all_results = []
    for filename, contributions in interviews:
        full_text = ' '.join([contrib.text for _, contrib in contributions])
        idea_buildup_score = calculate_idea_buildup(full_text)
        results = analyze_interview(filename, contributions)
        for result in results:
            result['idea_buildup_score'] = idea_buildup_score
        all_results.extend(results)

    # Write results to CSV (keep this for backward compatibility if needed)
    csv_file_path = os.path.join(config['input']['input_directory'], config['input']['main_file'])
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['Persona', 'Iteration', 'Tech_Score', 'Ethics_Score', 'Edu_Score', 'Idea_Buildup_Score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in all_results:
            writer.writerow({
                'Persona': result['filename'],
                'Iteration': result['iteration'],
                'Tech_Score': result['tech_score'],
                'Ethics_Score': result['ethics_score'],
                'Edu_Score': result['education_score'],
                'Idea_Buildup_Score': result['idea_buildup_score']
            })
    print(f"Results written to {csv_file_path}")

    print("\nPerforming I2S statistical analysis...")
    summary_stats, full_data, tech_ranking, tfidf_ranking, idea_buildup_ranking = perform_statistical_analysis(config)

    # Update the interviews2statistics_results.csv file
    update_results_csv(config, summary_stats, tech_ranking, idea_buildup_ranking, all_results)

    # Save rankings (keep this for backward compatibility if needed)
    save_rankings(config, tech_ranking, tfidf_ranking, idea_buildup_ranking)

    print("\nGenerating I2S charts...")
    generate_charts(config)

    # Compute and display correlation table
    correlation_columns = ['Tech_Score', 'Ethics_Score', 'Edu_Score', 'Idea_Buildup_Score']
    if 'TFIDF' in full_data.columns:
        correlation_columns.append('TFIDF')
    correlation_matrix = full_data[correlation_columns].corr()
    
    print("\nI2S Correlation Table:")
    print(correlation_matrix.to_string())

    print("\nI2S Rankings Comparison:")
    comparison = tech_ranking[['Persona', 'Tech_Score', 'Tech_Rank']]
    if tfidf_ranking is not None:
        comparison = pd.merge(comparison, 
                              tfidf_ranking[['Persona', 'TFIDF', 'TFIDF_Rank']], 
                              on='Persona')
    comparison = pd.merge(comparison,
                          idea_buildup_ranking[['Persona', 'Idea_Buildup_Score', 'Idea_Buildup_Rank']],
                          on='Persona')
    print(comparison.to_string(index=False))

if __name__ == "__main__":
    main()
