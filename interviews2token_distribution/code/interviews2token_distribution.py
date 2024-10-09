# File: interviews2token_distribution.py

import pandas as pd
import os


from sub.similarity import calculate_kl_divergence, calculate_cosine_similarity, calculate_js_divergence, save_matrices
from sub.visualization import plot_token_distribution
from sub.matrix_visualization import visualize_matrices
from sub.config_utility import load_config
from sub.data_transformation import generate_rectangular_data, calculate_divergences
from sub.divergence_line_chart import create_divergence_line_chart
from sub.distribution_analysis import process_distributions



def main():
    print("Running updated version of interviews2token_distribution.py")
        
    
    config_path = os.path.join(os.path.dirname(__file__), '../config/config.yaml')
    config = load_config(config_path)

    png_output_dir = config['png_output_dir']

    for calc_config in config['divergence_calculations']:
        calc_type = calc_config['type']
        origin = calc_config.get('origin', None)
        
        all_rectangular_data = []
        
        for input_config in config['input_files']:
            input_file = input_config['file']
            iterations = input_config['iterations']
            
            print(f"\nProcessing file: {input_file} for {calc_type}")
            
            # Load token distribution data
            token_df = pd.read_csv(input_file)
            
            # Filter data based on calculation type and origin
            if calc_type == "interview_focus_group":
                filtered_df = token_df
            elif calc_type in ["persona_nonpersona", "reference"] and origin:
                filtered_df = token_df[token_df['Origin'] == origin]
            else:
                print(f"Unsupported calculation type: {calc_type}")
                continue
            
            if filtered_df.empty:
                print(f"No data for {calc_type} in {input_file}")
                continue
            
            print(f"Shape of filtered data: {filtered_df.shape}")
            print(f"Unique Personas in filtered data: {filtered_df['Persona'].unique()}")

            # Calculate divergences
            divergences = calculate_divergences(filtered_df, calc_type=calc_type, origin=origin, top_n_tokens=config.get('top_n_tokens', 1000))
            
            print(f"\nCalculated divergences for {calc_type}:")
            for key, value in divergences.items():
                print(f"{key}: {value}")

            # Generate rectangular data
            rectangular_data = generate_rectangular_data(filtered_df, iterations, divergences, calc_type=calc_type, origin=origin)
            all_rectangular_data.append(rectangular_data)

        if all_rectangular_data:
            # Combine all rectangular data for this calculation type
            combined_rectangular_data = pd.concat(all_rectangular_data, ignore_index=True)

            # Create KL divergence line chart
            kl_chart_output = os.path.join(png_output_dir, f'kl_divergence_{calc_type}{"_" + origin if origin else ""}.png')
            create_divergence_line_chart(combined_rectangular_data, kl_chart_output, 'KL_divergence', f"{calc_type}_{origin if origin else ''}")

            # Create JS divergence line chart
            js_chart_output = os.path.join(png_output_dir, f'js_divergence_{calc_type}{"_" + origin if origin else ""}.png')
            create_divergence_line_chart(combined_rectangular_data, js_chart_output, 'JS_divergence', f"{calc_type}_{origin if origin else ''}")
        else:
            print(f"No data to create charts for {calc_type}")

    print("Processing completed successfully.")

if __name__ == "__main__":
    main()