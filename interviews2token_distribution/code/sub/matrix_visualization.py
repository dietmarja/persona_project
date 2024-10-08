import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sub.config_utility import load_config

def visualize_matrices(config_path):
    """
    Visualizes KL Divergence, Cosine Similarity, and JS Divergence matrices by reading the CSV files
    specified in the YAML config file and saving them as images in the output directory.
    """
    # Load the config
    config = load_config(config_path)
    
    kl_file = config['kl_divergence_file']
    cosine_file = config['cosine_similarity_file']
    js_file = config['js_divergence_file']
    output_dir = config['png_output_dir']
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Read and visualize the KL Divergence matrix
    kl_data = pd.read_csv(kl_file, index_col=0)
    print(f"KL Divergence Matrix:\n{kl_data}")
    
    kl_image_path = os.path.join(output_dir, 'kl_divergence_matrix.png')
    save_matrix_as_image(kl_data, kl_image_path, "KL Divergence Matrix")
    
    # Read and visualize the Cosine Similarity matrix
    cosine_data = pd.read_csv(cosine_file, index_col=0)
    print(f"Cosine Similarity Matrix:\n{cosine_data}")
    
    cosine_image_path = os.path.join(output_dir, 'cosine_similarity_matrix.png')
    save_matrix_as_image(cosine_data, cosine_image_path, "Cosine Similarity Matrix")
    
    # Read and visualize the JS Divergence matrix
    js_data = pd.read_csv(js_file, index_col=0)
    print(f"JS Divergence Matrix:\n{js_data}")
    
    js_image_path = os.path.join(output_dir, 'js_divergence_matrix.png')
    save_matrix_as_image(js_data, js_image_path, "JS Divergence Matrix")

def save_matrix_as_image(matrix, file_path, title):
    """
    Saves the given matrix as a heatmap image using Seaborn.
    
    Args:
    - matrix: DataFrame, the matrix to be visualized (with Persona as the index).
    - file_path: str, path to save the heatmap image.
    - title: str, the title of the heatmap.
    """
    try:
        # Print matrix dimensions and content for debugging
        print(f"Saving matrix: {title}")
        print(f"Matrix shape: {matrix.shape}")
        print(f"Matrix content:\n{matrix.head()}")

        # Ensure the output directory exists
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Check for and replace 'inf' values with NaN
        matrix = matrix.replace([np.inf, -np.inf], np.nan)

        # Print matrix after cleaning for debugging
        print(f"Matrix after replacing 'inf' values:\n{matrix.head()}")

        # Fill NaN with a large value for visualization purposes
        matrix.fillna(matrix.max().max() * 2, inplace=True)

        # Create the heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(matrix, annot=True, cmap='coolwarm', fmt=".2f", cbar=True)
        plt.title(title)
        plt.tight_layout()

        # Save the heatmap image
        print(f"Saving heatmap to: {file_path}")
        plt.savefig(file_path)

        # Close the figure to free up memory
        plt.close()

        print(f"Heatmap successfully saved to {file_path}")
    except Exception as e:
        print(f"Error saving matrix image for {title}: {e}")
