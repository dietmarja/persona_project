# code/sub/analysis3.py

import os
import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import string

def simple_tokenize(text):
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    return text.split()

def preprocess_text(text):
    stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
    tokens = simple_tokenize(text)
    return [word for word in tokens if word not in stop_words]

def calculate_lexical_diversity(text):
    tokens = preprocess_text(text)
    return len(set(tokens)) / len(tokens)

def calculate_unique_word_usage(text, corpus_vocab):
    tokens = set(preprocess_text(text))
    return len(tokens - corpus_vocab) / len(corpus_vocab)

def analyze_sentence_complexity(text):
    sentences = re.split(r'[.!?]+', text)
    word_counts = [len(simple_tokenize(sentence.strip())) for sentence in sentences if sentence.strip()]
    return np.mean(word_counts), np.std(word_counts)

def calculate_creativity_score(text, tfidf_matrix, feature_names, corpus_vocab):
    lexical_diversity = calculate_lexical_diversity(text)
    unique_word_usage = calculate_unique_word_usage(text, corpus_vocab)
    sentence_length_mean, sentence_length_std = analyze_sentence_complexity(text)
    
    tfidf_score = np.sum(np.sort(tfidf_matrix.toarray()[0])[-10:])  # Top 10 TF-IDF terms
    
    # Normalize and combine scores
    creativity_score = (
        0.3 * lexical_diversity +
        0.3 * unique_word_usage +
        0.2 * (sentence_length_mean / 30) +  # Normalized to be in similar range
        0.1 * (sentence_length_std / 10) +   # Normalized to be in similar range
        0.1 * tfidf_score                    # Already in a good range
    )
    
    return creativity_score

def analyze_creativity(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    texts = []
    persona_names = []
    all_tokens = set()

    for file in files:
        with open(os.path.join(directory, file), 'r') as f:
            content = f.read()
            texts.append(content)
            persona_names.append(file.replace('_interview.txt', '').replace('_', ' ').title())
            all_tokens.update(preprocess_text(content))

    corpus_vocab = all_tokens

    tfidf_vectorizer = TfidfVectorizer(max_features=1000, tokenizer=simple_tokenize)
    tfidf_matrix = tfidf_vectorizer.fit_transform(texts)
    feature_names = tfidf_vectorizer.get_feature_names_out()

    results = []
    for i, (persona, text) in enumerate(zip(persona_names, texts)):
        creativity_score = calculate_creativity_score(text, tfidf_matrix[i], feature_names, corpus_vocab)
        sentence_length_mean, sentence_length_std = analyze_sentence_complexity(text)
        lexical_diversity = calculate_lexical_diversity(text)
        unique_word_usage = calculate_unique_word_usage(text, corpus_vocab)

        results.append({
            'Persona': persona,
            'Creativity Score': creativity_score,
            'Lexical Diversity': lexical_diversity,
            'Unique Word Usage': unique_word_usage,
            'Avg Sentence Length': sentence_length_mean,
            'Sentence Length Std': sentence_length_std
        })

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('Creativity Score', ascending=False)

    return results_df

def perform_creativity_analysis(config):
    print("Performing creativity analysis...")
    results = analyze_creativity(config['input']['directory'])
    
    output_file = os.path.join(config['output']['directory'], 'creativity_analysis.csv')
    results.to_csv(output_file, index=False)
    print(f"Creativity analysis results saved to {output_file}")

    print("\nTop Most Creative Personas:")
    print(results)

    return results