from sub.similarity import calculate_kl_divergence, calculate_cosine_similarity, calculate_js_divergence, save_matrices
from sub.visualization import plot_token_distribution
from sub.matrix_visualization import visualize_matrices
from sub.config_utility import load_config
from sub.data_transformation import generate_rectangular_data, calculate_divergences
from sub.kl_divergence_line_chart import create_kl_divergence_line_chart
import pandas as pd
import os

def main():
    print("Running updated version of interviews2token_distribution.py")
    
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '../config/config.yaml')
    config = load_config(config_path)
    
    # Extract paths from config
    kl_file = config['kl_divergence_file']
    cosine_file = config['cosine_similarity_file']
    js_file = config['js_divergence_file']
    png_output_dir = config['png_output_dir']
    kl_chart_output = config['kl_divergence_line_chart']

    # Process each input file
    all_rectangular_data = []
    for input_config in config['input_files']:
        input_file = input_config['file']
        iterations = input_config['iterations']
        
        print(f"Processing file: {input_file}")
        
        # Load token distribution data
        token_df = pd.read_csv(input_file)
        print(f"Columns in {input_file}:", token_df.columns)

        # Calculate divergences
        divergences = calculate_divergences(token_df)

        # Generate rectangular data
        rectangular_data = generate_rectangular_data(token_df, iterations, divergences)
        all_rectangular_data.append(rectangular_data)

        # Create matrices
        personas_origins = list(divergences.keys())
        kl_matrix = pd.DataFrame({p_o: d['KL_divergence'] for p_o, d in divergences.items()}, index=personas_origins)
        cosine_matrix = pd.DataFrame({p_o: d['cosine_similarity'] for p_o, d in divergences.items()}, index=personas_origins)
        js_matrix = pd.DataFrame({p_o: d['JS_divergence'] for p_o, d in divergences.items()}, index=personas_origins)

        # Save the matrices
        save_matrices(kl_matrix, cosine_matrix, js_matrix, kl_file, cosine_file, js_file)

        # Plot token distributions
        plot_token_distribution(token_df, png_output_dir)

    # Combine all rectangular data
    combined_rectangular_data = pd.concat(all_rectangular_data, ignore_index=True)

    # Debug information
    print("\nCombined Data Information:")
    print(combined_rectangular_data)
    print("\nData types:")
    print(combined_rectangular_data.dtypes)
    print("\nUnique Personas in data:", combined_rectangular_data['Persona'].unique())
    print("Unique Origins in data:", combined_rectangular_data['Origin'].unique())
    print("Unique Iterations in data:", combined_rectangular_data['Iteration'].unique())
    print("\nSample of KL_divergence values:")
    print(combined_rectangular_data['KL_divergence'].head(10))
    print("\nUnique KL_divergence values:")
    print(combined_rectangular_data['KL_divergence'].unique())

    # Ensure 'combined' is not in the Origin column
    if 'combined' in combined_rectangular_data['Origin'].unique():
        print("Warning: 'combined' found in Origin column. Removing these entries.")
        combined_rectangular_data = combined_rectangular_data[combined_rectangular_data['Origin'] != 'combined']

    # Visualize matrices
    visualize_matrices(config_path)

    # Create KL divergence line chart
    if 'KL_divergence' in combined_rectangular_data.columns:
        create_kl_divergence_line_chart(combined_rectangular_data, kl_chart_output)
    else:
        print("Warning: KL_divergence data not available. Skipping KL divergence line chart.")

if __name__ == "__main__":
    main()

# Update the generate_rectangular_data function in sub/data_transformation.py
def generate_rectangular_data(token_df, iterations, divergences):
    rectangular_data = []
    
    for persona in token_df['Persona'].unique():
        for origin in ['interview', 'focus_group']:
            if (persona, origin) in divergences:
                kl_divergence = divergences[(persona, origin)]['KL_divergence']
                js_divergence = divergences[(persona, origin)]['JS_divergence']
                
                rectangular_data.append({
                    'Persona': persona,
                    'Origin': origin,
                    'Iteration': iterations,
                    'KL_divergence': kl_divergence,
                    'JS_divergence': js_divergence
                })
    
    return pd.DataFrame(rectangular_data)
