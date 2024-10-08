import numpy as np
from scipy.stats import entropy
from scipy.spatial.distance import jensenshannon

def calculate_kl_divergence(p, q):
    # Add a small epsilon to avoid division by zero
    epsilon = 1e-10
    p = p + epsilon
    q = q + epsilon
    
    # Normalize
    p = p / p.sum()
    q = q / q.sum()
    
    return entropy(p, q)

def calculate_js_divergence(p, q):
    # Add a small epsilon to avoid division by zero
    epsilon = 1e-10
    p = p + epsilon
    q = q + epsilon
    
    # Normalize
    p = p / p.sum()
    q = q / q.sum()
    
    return jensenshannon(p, q)


def calculate_cosine_similarity(distribution1, distribution2):
    """
    Calculate cosine similarity between two distributions.
    
    Args:
    distribution1 (pd.Series or pd.DataFrame): First distribution
    distribution2 (pd.Series): Second distribution (reference)
    
    Returns:
    float or pd.Series: Cosine similarity(ies)
    """
    # Ensure both distributions have the same index
    common_index = distribution1.index.intersection(distribution2.index)
    dist1 = distribution1.loc[common_index]
    dist2 = distribution2.loc[common_index]
    
    if isinstance(distribution1, pd.DataFrame):
        return dist1.apply(lambda col: np.dot(col, dist2) / (np.linalg.norm(col) * np.linalg.norm(dist2)))
    else:
        return np.dot(dist1, dist2) / (np.linalg.norm(dist1) * np.linalg.norm(dist2))


def save_matrices(kl_matrix, js_matrix, kl_file, js_file):
    print("Saving KL Divergence Matrix")
    kl_matrix.to_csv(kl_file)
    print(f"KL Divergence matrix saved to {kl_file}")

    print("Saving JS Divergence Matrix")
    js_matrix.to_csv(js_file)
    print(f"JS Divergence matrix saved to {js_file}")