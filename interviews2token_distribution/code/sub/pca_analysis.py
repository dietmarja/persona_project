# sub/pca_analysis.py

import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def run_pca(divergence_matrix, n_components=2):
    similarity_matrix = np.exp(-divergence_matrix)
    scaler = StandardScaler()
    similarity_matrix_standardized = scaler.fit_transform(similarity_matrix)
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(similarity_matrix_standardized)
    return principal_components, pca.explained_variance_ratio_

def perform_pca_analysis(token_df, divergence_type='js', n_components=2):
    from .data_transformation import create_pairwise_divergence_matrix
    distributions = [token_df[token_df['Interview'] == i].set_index('Token')['Count'] for i in token_df['Interview'].unique()]
    divergence_matrix = create_pairwise_divergence_matrix(distributions, divergence_type)
    principal_components, explained_variance_ratio = run_pca(divergence_matrix, n_components)
    return principal_components, explained_variance_ratio