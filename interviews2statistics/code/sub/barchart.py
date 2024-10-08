# File: code/sub/barchart.py

import matplotlib.pyplot as plt
import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)

def generate_charts(config):
    # Placeholder for the original generate_charts function
    # Keep this if it's used elsewhere in your project
    logging.info("generate_charts function called")
    # Implementation of generate_charts
    pass

def generate_tech_score_chart(config, summary_stats):
    logging.debug("generate_tech_score_chart function called")
    
    # Ensure the output directory exists
    charts_directory = config['output']['charts_directory']
    os.makedirs(charts_directory, exist_ok=True)

    # Calculate the difference from the 'no_persona' score
    no_persona_score = summary_stats[summary_stats['filename'] == 'no_persona_interview.txt']['tech_score_mean'].values[0]
    summary_stats['score_difference'] = summary_stats['tech_score_mean'] - no_persona_score

    # Sort by score difference in descending order
    summary_stats_sorted = summary_stats.sort_values('score_difference', ascending=True)

    # Calculate the number of personas
    num_personas = len(summary_stats_sorted)

    # Create the horizontal bar chart with adjusted figure size
    fig, ax = plt.subplots(figsize=(10, num_personas * 0.25))  # Adjust height based on number of personas

    bars = ax.barh(range(num_personas), summary_stats_sorted['score_difference'], height=0.8)  # Keep bar height at 0.8

    # Color the bars based on positive (blue) or negative (red) difference
    for bar in bars:
        if bar.get_width() < 0:
            bar.set_color('red')
        else:
            bar.set_color('blue')

    # Customize the chart
    ax.set_title('Normalized Tech Score by Persona', fontsize=12, pad=5)
    ax.set_xlabel('Difference from Plain LLM Score', fontsize=10)
    ax.set_ylabel('Persona', fontsize=10)

    # Remove the .txt extension from filenames for cleaner labels
    labels = [label.replace('_interview.txt', '').replace('_', ' ').title() for label in summary_stats_sorted['filename']]
    ax.set_yticks(range(num_personas))
    ax.set_yticklabels(labels, fontsize=8)

    # Add gridlines for readability
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Adjust layout manually to remove extra white space
    fig.subplots_adjust(left=0.3, right=0.95, top=0.98, bottom=0.05)

    # Save the chart with minimal padding
    chart_path = os.path.join(charts_directory, 'tech_score_chart.pdf')
    plt.savefig(chart_path, bbox_inches='tight', pad_inches=0.01)
    plt.close()

    logging.debug(f"Tech score chart saved to {chart_path}")

# Keep the generate_charts function if it's still needed
def generate_charts(config):
    logging.debug("generate_charts function called")

# If you want to test the functions directly from this file
if __name__ == "__main__":
    # You could add some test code here if needed
    pass
