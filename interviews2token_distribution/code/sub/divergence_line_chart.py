# File: sub/divergence_line_chart.py

import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_divergence_line_chart(data, output_path, divergence_type, chart_type):
    plt.figure(figsize=(12, 8))
    sns.set_style("whitegrid")
    
    for persona in data['Persona'].unique():
        persona_data = data[data['Persona'] == persona]
        plt.plot(persona_data['Iteration'], persona_data[divergence_type], 
                 marker='o', linestyle='-', linewidth=2, markersize=8, label=persona)
    
    plt.xlabel('Iteration', fontsize=14)
    plt.ylabel(f'Normalized {divergence_type.replace("_", " ")}', fontsize=14)
    
    if chart_type.startswith("interview_focus_group"):
        title = f'Normalized {divergence_type.replace("_", " ")} (Interview vs Focus Group)'
    elif chart_type.startswith("persona_nonpersona"):
        origin = chart_type.split('_')[-1]
        title = f'Normalized {divergence_type.replace("_", " ")} (Persona vs No Persona, {origin.capitalize()})'
    elif chart_type.startswith("reference"):
        origin = chart_type.split('_')[-1]
        title = f'Normalized {divergence_type.replace("_", " ")} to Reference Distribution ({origin.capitalize()})'
    else:
        title = f'Normalized {divergence_type.replace("_", " ")}'
    
    plt.title(title, fontsize=16)
    plt.legend(title='Persona', title_fontsize='13', fontsize='12', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"{divergence_type} line chart for {chart_type} saved to {output_path}")