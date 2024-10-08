# File: code/sub/barchart.py

import matplotlib.pyplot as plt
import pandas as pd
import os

def generate_charts(config):
    # Placeholder for the original generate_charts function
    # You may want to keep this if it's used elsewhere in your project
    pass

def generate_tech_score_chart(config, summary_stats):
    # Ensure the output directory exists
    os.makedirs(config['output']['charts_directory'], exist_ok=True)

    # Calculate the difference from the 'no_persona' score
    no_persona_score = summary_stats[summary_stats['filename'] == 'no_persona_interview.txt']['tech_score_mean'].values[0]
    summary_stats['score_difference'] = summary_stats['tech_score_mean'] - no_persona_score

    # Sort by score difference in descending order
    summary_stats_sorted = summary_stats.sort_values('score_difference', ascending=True)

    # Create the horizontal bar chart
    plt.figure(figsize=(12, 20))  # Adjust the figure size as needed
    bars = plt.barh(summary_stats_sorted['filename'], summary_stats_sorted['score_difference'])

    # Color the bars based on positive (blue) or negative (red) difference
    for bar in bars:
        if bar.get_width() < 0:
            bar.set_color('red')
        else:
            bar.set_color('blue')

    # Customize the chart
    plt.title('Normalized Tech Score by Persona')
    plt.xlabel('Difference from Plain LLM Score')
    plt.ylabel('Persona')

    # Remove the .txt extension from filenames for cleaner labels
    labels = [label.replace('_interview.txt', '').replace('_', ' ').title() for label in summary_stats_sorted['filename']]
    plt.yticks(range(len(labels)), labels)

    # Add gridlines for readability
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    # Adjust layout and save the chart
    plt.tight_layout()
    chart_path = os.path.join(config['output']['charts_directory'], 'tech_score_chart.pdf')
    plt.savefig(chart_path)
    plt.close()

    print(f"Tech score chart saved to {chart_path}")

# If you want to test the function directly from this file
if __name__ == "__main__":
    # You could add some test code here if needed
    pass
