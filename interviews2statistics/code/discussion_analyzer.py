# code/discussion_analyzer.py

import csv
import os
import sys
import yaml
import pandas as pd
from datetime import datetime
from sub.file_processing import read_discussions_from_directory
from sub.analysis1 import analyze_discussion
from sub.analysis2 import perform_statistical_analysis
from sub.barchart import generate_charts

def save_rankings(config, tech_ranking, tfidf_ranking):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"rankings_{timestamp}.txt"
    output_file = os.path.join(config['output']['stat_results_directory'], filename)
    
    with open(output_file, 'w') as f:
        f.write("Tech Score Ranking:\n")
        f.write(tech_ranking[['Persona', 'Tech_Score', 'Tech_Rank']].to_string(index=False))
        f.write("\n\nTFIDF Ranking:\n")
        f.write(tfidf_ranking[['Persona', 'TFIDF', 'TFIDF_Rank']].to_string(index=False))
    
    print(f"Rankings saved to {output_file}")

def main():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    print("Starting analysis...")
    discussions = read_discussions_from_directory(config['input']['input_directory'])
    
    if not discussions:
        print("No valid discussions found in the specified directory.")
        return

    all_results = []
    for filename, contributions in discussions:
        results = analyze_discussion(filename, contributions)
        all_results.extend(results)

    csv_file_path = os.path.join(config['input']['input_directory'], config['input']['main_file'])
    # Ensure directory exists
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['Persona', 'Iteration', 'Tech_Score', 'Ethics_Score', 'Edu_Score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in all_results:
            writer.writerow({
                'Persona': result['filename'],
                'Iteration': result['iteration'],
                'Tech_Score': result['tech_score'],
                'Ethics_Score': result['ethics_score'],
                'Edu_Score': result['education_score']
            })
    print(f"Results written to {csv_file_path}")

    print("\nPerforming statistical analysis...")
    summary_stats, full_data, tech_ranking, tfidf_ranking = perform_statistical_analysis(config)

    # Save rankings
    save_rankings(config, tech_ranking, tfidf_ranking)

    print("\nGenerating charts...")
    generate_charts(config)

    # Compute and display correlation table at the end
    correlation_columns = ['Tech_Score', 'TFIDF']
    correlation_matrix = full_data[correlation_columns].corr()
    
    print("\nCorrelation Table:")
    print(correlation_matrix.to_string())

    print("\nRankings Comparison:")
    comparison = pd.merge(tech_ranking[['Persona', 'Tech_Score', 'Tech_Rank']], 
                          tfidf_ranking[['Persona', 'TFIDF', 'TFIDF_Rank']], 
                          on='Persona')
    print(comparison.to_string(index=False))

if __name__ == "__main__":
    main()