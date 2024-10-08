import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

def create_kl_divergence_line_chart(data, output_path):
    plt.clf()
    plt.close('all')
    sns.reset_orig()
    
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(12, 8))
    
    print("Shape of data:", data.shape)
    print("Columns in data:", data.columns)
    print("Data types:")
    print(data.dtypes)
    print("\nFirst few rows of data:")
    print(data)
    
    personas = data['Persona'].unique()
    color_palette = sns.color_palette("husl", n_colors=len(personas))
    color_dict = dict(zip(personas, color_palette))
    
    legend_elements = []
    
    for persona in personas:
        persona_data = data[data['Persona'] == persona]
        
        for origin in persona_data['Origin'].unique():
            origin_data = persona_data[persona_data['Origin'] == origin]
            
            if not origin_data.empty:
                linestyle = '-' if origin == 'interview' else '--'
                
                print(f"\nRaw data for {persona} ({origin}):")
                print(origin_data[['Iteration', 'KL_divergence']])
                
                # Convert KL_divergence to float, replacing None with NaN
                origin_data['KL_divergence'] = pd.to_numeric(origin_data['KL_divergence'], errors='coerce')
                
                # Remove rows with NaN KL_divergence
                valid_data = origin_data.dropna(subset=['KL_divergence'])
                
                if not valid_data.empty:
                    line, = ax.plot(valid_data['Iteration'], valid_data['KL_divergence'], 
                            marker='o', linestyle=linestyle, linewidth=2, markersize=8,
                            label=f"{persona} ({origin})", color=color_dict[persona])
                    legend_elements.append(line)
                    print(f"Successfully plotted data for {persona} ({origin})")
                else:
                    print(f"No valid data to plot for {persona} ({origin})")
            else:
                print(f"No data found for {persona} ({origin})")
    
    ax.set_xlabel('Iteration', fontsize=14)
    ax.set_ylabel('KL Divergence', fontsize=14)
    ax.set_title('KL Divergence Over Iterations by Persona and Origin', fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Set x-axis ticks to only show the actual iteration values
    ax.set_xticks(data['Iteration'].unique())
    ax.set_xticklabels(data['Iteration'].unique())
    
    if legend_elements:
        ax.legend(handles=legend_elements, title='Persona (Origin)', title_fontsize='13', fontsize='12', loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        print("Warning: No lines were plotted, so no legend was created")
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    print(f"KL Divergence line chart saved to {output_path}")
    
    plotted_personas = set(persona for persona, origin in [element.get_label().split(' (') for element in legend_elements])
    plotted_origins = set(origin.rstrip(')') for persona, origin in [element.get_label().split(' (') for element in legend_elements])
    print("Plotted Personas:", plotted_personas)
    print("Plotted Origins:", plotted_origins)
