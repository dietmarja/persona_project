# code/sub/charts.py

import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from scipy import stats

def format_persona_name(name):
    if name.lower() == 'no persona':
        return "Plain LLM"
    
    words = name.split()
    formatted_words = []
    for word in words:
        if word.lower() == 'ai':
            formatted_words.append('AI')
        elif word.lower() in ['and', 'of', 'in', 'at', 'the', 'for', 'to']:
            formatted_words.append(word.lower())
        else:
            formatted_words.append(word.capitalize())
    
    return ' '.join(formatted_words)

def create_compact_grouped_bar_chart(config):
    tech_score_file = os.path.join(config['input']['directory'], config['input']['main_file'])
    creativity_score_file = os.path.join(config['output']['directory'], 'creativity_analysis.csv')
    
    tech_data = pd.read_csv(tech_score_file)
    creativity_data = pd.read_csv(creativity_score_file)
    
    # Ensure all personas are included
    all_personas = pd.concat([tech_data['Persona'], creativity_data['Persona']]).unique()
    
    # Create a DataFrame with all personas
    merged_data = pd.DataFrame({'Persona': all_personas})
    
    # Merge with tech and creativity data
    merged_data = merged_data.merge(tech_data[['Persona', 'Tech_Score']], on='Persona', how='left')
    merged_data = merged_data.merge(creativity_data[['Persona', 'Creativity Score', 'Lexical Diversity']], on='Persona', how='left')
    
    # Apply formatting to persona names
    merged_data['Formatted_Persona'] = merged_data['Persona'].apply(format_persona_name)
    
    # Sort by Tech Score
    merged_data = merged_data.sort_values('Tech_Score', ascending=True)
    
    # Create the grouped bar chart
    fig, ax = plt.subplots(figsize=(12, 10))
    
    y = np.arange(len(merged_data['Formatted_Persona']))
    height = 0.2
    
    # Plot scores
    tech_bars = ax.barh(y, merged_data['Tech_Score'], height, color='blue', alpha=0.7, label='Tech Score')
    creativity_bars = ax.barh(y + height, merged_data['Creativity Score'], height, color='green', alpha=0.7, label='Creativity Score')
    lexical_bars = ax.barh(y + 2*height, merged_data['Lexical Diversity'], height, color='red', alpha=0.7, label='Lexical Diversity')
    
    ax.set_title('Tech Score, Creativity Score, and Lexical Diversity by Persona', fontsize=16)
    ax.set_xlabel('Score', fontsize=12)
    ax.set_yticks(y + height)
    ax.set_yticklabels(merged_data['Formatted_Persona'])
    
    ax.legend(loc='lower right', fontsize=10)
    plt.tight_layout()
    
    # Display values on bars
    def autolabel(rects):
        for rect in rects:
            width = rect.get_width()
            if not np.isnan(width):
                ax.annotate(f'{width:.2f}', xy=(width, rect.get_y() + rect.get_height()/2),
                            xytext=(3, 0), textcoords="offset points", ha='left', va='center')

    for bars in [tech_bars, creativity_bars, lexical_bars]:
        autolabel(bars)
    
    output_file = os.path.join(config['output']['directory'], config['output']['charts_directory'], 'scores_comparison_chart.png')
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close()
    
    print(f"Scores comparison chart saved to {output_file}")

    # Calculate correlations only for personas with both scores
    valid_data = merged_data.dropna(subset=['Tech_Score', 'Creativity Score', 'Lexical Diversity'])
    
    correlations = {}
    if len(valid_data) > 1:  # Need at least two points for correlation
        correlations['Creativity Score'] = stats.pearsonr(valid_data['Tech_Score'], valid_data['Creativity Score'])[0]
        correlations['Lexical Diversity'] = stats.pearsonr(valid_data['Tech_Score'], valid_data['Lexical Diversity'])[0]
    
        print("\nCorrelations with Tech Score:")
        for method, corr in correlations.items():
            print(f"{method}: {corr:.4f}")
    else:
        print("\nNot enough data to calculate correlations.")

    # Print personas with missing scores
    print("\nPersonas with missing scores:")
    missing_tech = merged_data[merged_data['Tech_Score'].isna()]['Formatted_Persona'].tolist()
    missing_creativity = merged_data[merged_data['Creativity Score'].isna()]['Formatted_Persona'].tolist()
    
    if missing_tech:
        print("Missing Tech Score:", ', '.join(missing_tech))
    if missing_creativity:
        print("Missing Creativity Score:", ', '.join(missing_creativity))

def generate_charts(config):
    create_compact_grouped_bar_chart(config)