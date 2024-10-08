import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

def create_kl_divergence_line_chart(data, output_path):
    """
    Create a line chart of KL divergence over Iterations for each Persona and Origin.
    
    Args:
    data (pd.DataFrame): DataFrame containing the data
    output_path (str): Path to save the output image
    """
    # Reset matplotlib and seaborn
    plt.clf()
    plt.close('all')
    sns.reset_orig()
    
    # Set the style for the chart
    plt.style.use('seaborn')
    
    # Create a new figure and axis objects
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Get unique personas and assign a color to each
    personas = data['Persona'].unique()
    color_palette = sns.color_palette("husl", n_colors=len(personas))
    color_dict = dict(zip(personas, color_palette))
    
    # Plot a line for each persona and origin
    for persona in personas:
        persona_data = data[data['Persona'] == persona]
        
        for origin in persona_data['Origin'].unique():
            origin_data = persona_data[persona_data['Origin'] == origin]
            linestyle = '-' if origin == 'interview' else '--'
            
            ax.plot(origin_data['Iteration'], origin_data['KL_divergence'], 
                    marker='o', linestyle=linestyle, linewidth=2, markersize=8,
                    label=f"{persona} ({origin})", color=color_dict[persona])
    
    # Customize the chart
    ax.set_xlabel('Iteration', fontsize=14)
    ax.set_ylabel('KL Divergence', fontsize=14)
    ax.set_title('KL Divergence Over Iterations by Persona and Origin', fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Add legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, title='Persona (Origin)', title_fontsize='13', fontsize='12', loc='center left', bbox_to_anchor=(1, 0.5))
    
    # Adjust layout and save
    plt.tight_layout()
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)  # Close the figure to free up memory
    
    print(f"KL Divergence line chart saved to {output_path}")

def load_data_and_create_kl_chart(data_path, output_path):
    """
    Load data from CSV and create the KL Divergence line chart.
    
    Args:
    data_path (str): Path to the CSV file containing the data
    output_path (str): Path to save the output image
    """
    # Load the data
    data = pd.read_csv(data_path)
    
    # Create the chart
    create_kl_divergence_line_chart(data, output_path)

# This part is optional - you can call this function directly from your main script
if __name__ == "__main__":
    data_path = "path/to/your/rectangular_data.csv"
    output_path = "path/to/save/kl_divergence_line_chart.png"
    load_data_and_create_kl_chart(data_path, output_path)
