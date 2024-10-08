# File: /Users/dietmar/Dropstack/PycharmProjects/interviews2statistics/code/sub/analysis2.py

import pandas as pd
import numpy as np
from scipy import stats

# File: /Users/dietmar/Dropstack/PycharmProjects/interviews2statistics/code/sub/analysis2.py

def perform_statistical_analysis(config, all_results):
    print("Starting statistical analysis...")
    
    # Create DataFrame from all_results
    df = pd.DataFrame(all_results)
    print("This is df!!")
    print(df)
    
    # Calculate summary statistics
    summary_stats = df.groupby('filename').agg({
        'tech_score': ['mean', 'std'],
        'ethics_score': ['mean', 'std'],
        'education_score': ['mean', 'std'],
        'idea_buildup_score': ['mean', 'std']
    })
    
    #filtered_stats = summary_stats[summary_stats['no_persona_interview.txt'] #== no_persona_file]
    #if filtered_stats.empty:
    #    print(f"No matching file found for {no_persona_file}")
    # Handle the case where no matching file is found
    
        
    print("\nSummary stats columns:")
    print(summary_stats.columns)
    
    # Flatten column names
    summary_stats.columns = ['_'.join(col).strip() for col in summary_stats.columns.values]
    
    print("\nFlattened summary stats columns:")
    print(summary_stats.columns)
    
    # Reset index to make 'filename' a column
    summary_stats = summary_stats.reset_index()
    
    print("\nFinal summary_stats:")
    print(summary_stats)
    
    # Create rankings based on mean scores
    tech_ranking = summary_stats[['filename', 'tech_score_mean']].sort_values('tech_score_mean', ascending=False).reset_index(drop=True)
    tech_ranking['Tech_Rank'] = tech_ranking.index + 1
    
    idea_buildup_ranking = summary_stats[['filename', 'idea_buildup_score_mean']].sort_values('idea_buildup_score_mean', ascending=False).reset_index(drop=True)
    idea_buildup_ranking['Idea_Buildup_Rank'] = idea_buildup_ranking.index + 1

    print("\nDebugging information from perform_statistical_analysis:")
    print("Tech ranking:")
    print(tech_ranking)
    print("\nTech ranking columns:", tech_ranking.columns)
    
    print("\nIdea buildup ranking:")
    print(idea_buildup_ranking)
    print("\nIdea buildup ranking columns:", idea_buildup_ranking.columns)

    # Perform correlation analysis
    correlation_matrix = df[['tech_score', 'ethics_score', 'education_score', 'idea_buildup_score']].corr()
    
    print("\nCorrelation Matrix:")
    print(correlation_matrix)
    
    tfidf_ranking = None  # Implement TFIDF ranking if needed
    anova_results = None  # Implement ANOVA if needed
    tukey_results = None  # Implement Tukey's HSD if needed
    model_results = None  # Implement mixed-effects model if needed
    
    print("Statistical analysis complete.")
    
    return summary_stats, df, tech_ranking, tfidf_ranking, idea_buildup_ranking, correlation_matrix, anova_results, tukey_results, model_results
