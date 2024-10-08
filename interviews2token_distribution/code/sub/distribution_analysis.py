# File: sub/distribution_analysis.py

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from sub.similarity import calculate_kl_divergence, calculate_js_divergence

def create_pairwise_divergence_matrix(distributions, divergence_type='js'):
    """
    Create a pairwise divergence matrix for given distributions.
    
    :param distributions: List of token distributions
    :param divergence_type: 'js' for Jensen-Shannon or 'kl' for Kullback-Leibler
    :return: Pairwise divergence matrix
    """
    n = len(distributions)
    divergence_func = calculate_js_divergence if divergence_type == 'js' else calculate_kl_divergence
    
    divergence_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1, n):
            div = divergence_func(distributions[i], distributions[j])
            divergence_matrix[i, j] = div
            divergence_matrix[j, i] = div
    
    return pd.DataFrame(divergence_matrix)

def find_closest_and_farthest_distributions(divergence_matrix, v, w):
    """
    Find v closest and w farthest distributions based on divergence scores.
    
    :param divergence_matrix: DataFrame of pairwise divergences
    :param v: Number of closest distributions to find
    :param w: Number of farthest distributions to find
    :return: Tuple of (v closest pairs, w farthest pairs)
    """
    # Convert upper triangle to 1D array
    tri_up = divergence_matrix.values[np.triu_indices(len(divergence_matrix), k=1)]
    
    # Find v smallest and w largest values
    closest_indices = np.argpartition(tri_up, v)[:v]
    farthest_indices = np.argpartition(tri_up, -w)[-w:]
    
    # Convert 1D indices back to 2D indices
    get_2d_indices = lambda idx: np.unravel_index(idx, (len(divergence_matrix), len(divergence_matrix)))
    closest_pairs = [get_2d_indices(idx) for idx in closest_indices]
    farthest_pairs = [get_2d_indices(idx) for idx in farthest_indices]
    
    return closest_pairs, farthest_pairs

def process_distributions(token_df, n, divergence_type='js', v=3, w=3):
    """
    Process n token distributions to create divergence matrix and find closest/farthest pairs.
    
    :param token_df: DataFrame containing token distributions
    :param n: Number of distributions to process
    :param divergence_type: Type of divergence to use ('js' or 'kl')
    :param v: Number of closest pairs to find
    :param w: Number of farthest pairs to find
    :return: Tuple of (divergence matrix, closest pairs, farthest pairs)
    """
    # Assuming token_df has columns: 'Interview', 'Token', 'Count'
    distributions = [token_df[token_df['Interview'] == i].set_index('Token')['Count'] 
                     for i in range(1, n+1)]
    
    divergence_matrix = create_pairwise_divergence_matrix(distributions, divergence_type)
    closest, farthest = find_closest_and_farthest_distributions(divergence_matrix, v, w)
    
    return divergence_matrix, closest, farthest