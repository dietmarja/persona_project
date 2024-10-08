# File: sub/data_transformation.py

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sub.similarity import calculate_kl_divergence, calculate_js_divergence

def create_reference_distribution(token_df, relevant_tokens):
    # Combine all tokens and their counts
    all_tokens = token_df.groupby('Token')['Count'].sum().reindex(relevant_tokens).fillna(0)
    
    # Scramble the counts
    scrambled_counts = np.random.permutation(all_tokens.values)
    
    # Create the reference distribution
    ref_dist = pd.Series(scrambled_counts, index=all_tokens.index)
    
    # Normalize
    return ref_dist / ref_dist.sum()

def normalize_divergences(divergences):
    min_kl = min(d['KL_divergence'] for d in divergences.values())
    min_js = min(d['JS_divergence'] for d in divergences.values())
    
    normalized_divergences = {}
    for persona, values in divergences.items():
        normalized_divergences[persona] = {
            'KL_divergence': values['KL_divergence'] - min_kl,
            'JS_divergence': values['JS_divergence'] - min_js
        }
    
    return normalized_divergences


def calculate_divergences(token_df, calc_type, origin=None, top_n_tokens=1000):
    # Create a document for each persona and origin
    documents = []
    doc_labels = []
    for persona in token_df['Persona'].unique():
        for org in token_df['Origin'].unique():
            persona_origin_data = token_df[(token_df['Persona'] == persona) & (token_df['Origin'] == org)]
            doc = ' '.join([token + ' ' * int(count) for token, count in zip(persona_origin_data['Token'], persona_origin_data['Count'])])
            documents.append(doc)
            doc_labels.append((persona, org))
    
    # Calculate TF-IDF
    vectorizer = TfidfVectorizer(max_features=top_n_tokens if top_n_tokens > 0 else None)
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Get the most relevant tokens
    relevant_tokens = vectorizer.get_feature_names_out()
    
    print(f"Number of relevant tokens selected: {len(relevant_tokens)}")

    # Create reference distribution
    ref_dist = create_reference_distribution(token_df, relevant_tokens)
    
    divergences = {}
    
    for persona in token_df['Persona'].unique():
        if origin:
            persona_data = token_df[(token_df['Persona'] == persona) & (token_df['Origin'] == origin)]
        else:
            persona_data = token_df[token_df['Persona'] == persona]
        
        persona_dist = create_distribution(persona_data, relevant_tokens)
        
        kl_div = calculate_kl_divergence(ref_dist, persona_dist)
        js_div = calculate_js_divergence(ref_dist, persona_dist)
        
        divergences[persona] = {'KL_divergence': kl_div, 'JS_divergence': js_div}
        
        # Debug information
        print(f"Persona: {persona}")
        print(f"Distribution shape: {persona_dist.shape}")
        print(f"Number of zero-padded tokens: {(persona_dist == 0).sum()}")
        print(f"KL divergence to reference: {kl_div}")
        print(f"JS divergence to reference: {js_div}")
    
    # Normalize divergences
    normalized_divergences = normalize_divergences(divergences)
    
    return normalized_divergences


def create_reference_distribution(token_df, relevant_tokens):
    # Combine all tokens and their counts
    all_tokens = token_df.groupby('Token')['Count'].sum().reindex(relevant_tokens).fillna(0)
    
    # Scramble the counts
    scrambled_counts = np.random.permutation(all_tokens.values)
    
    # Create the reference distribution
    ref_dist = pd.Series(scrambled_counts, index=all_tokens.index)
    
    # Normalize
    return ref_dist / ref_dist.sum()

def create_distribution(data, relevant_tokens):
    dist = pd.Series({token: data[data['Token'] == token]['Count'].sum() for token in relevant_tokens}).fillna(0)
    total = dist.sum()
    return dist / total if total > 0 else dist

def normalize_divergences(divergences):
    min_kl = min(d['KL_divergence'] for d in divergences.values())
    min_js = min(d['JS_divergence'] for d in divergences.values())
    
    normalized_divergences = {}
    for persona, values in divergences.items():
        normalized_divergences[persona] = {
            'KL_divergence': values['KL_divergence'] - min_kl,
            'JS_divergence': values['JS_divergence'] - min_js
        }
    
    return normalized_divergences



def create_distribution(data, relevant_tokens):
    dist = pd.Series({token: data[data['Token'] == token]['Count'].sum() for token in relevant_tokens}).fillna(0)
    total = dist.sum()
    return dist / total if total > 0 else dist

def generate_rectangular_data(token_df, iterations, divergences, calc_type, origin=None):
    rectangular_data = []
    
    for persona, div_values in divergences.items():
        rectangular_data.append({
            'Persona': persona,
            'Iteration': iterations,
            'KL_divergence': div_values['KL_divergence'],
            'JS_divergence': div_values['JS_divergence'],
            'Calculation_Type': calc_type,
            'Origin': origin
        })
    
    return pd.DataFrame(rectangular_data)
    

def create_distribution(data, relevant_tokens):
    # Create a distribution with all relevant tokens, filling with zeros for missing tokens
    dist = pd.Series({token: data[data['Token'] == token]['Count'].sum() for token in relevant_tokens}).fillna(0)
    
    # Normalize the distribution
    total_count = dist.sum()
    if total_count > 0:
        dist = dist / total_count
    else:
        # If all counts are zero, create a uniform distribution
        dist = pd.Series({token: 1/len(relevant_tokens) for token in relevant_tokens})
    
    return dist

def generate_rectangular_data(token_df, iterations, divergences, calc_type, origin=None):
    rectangular_data = []
    
    for persona, div_values in divergences.items():
        rectangular_data.append({
            'Persona': persona,
            'Iteration': iterations,
            'KL_divergence': div_values['KL_divergence'],
            'JS_divergence': div_values['JS_divergence'],
            'Calculation_Type': calc_type,
            'Origin': origin
        })
    
    return pd.DataFrame(rectangular_data)