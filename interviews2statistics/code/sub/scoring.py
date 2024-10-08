# sub/scoring.py

from collections import Counter
from nltk.tokenize import word_tokenize
import nltk

# Download necessary NLTK data
nltk.download('punkt', quiet=True)

# Define keyword lists (you may want to expand these)
tech_keywords = ['technology']
ethics_keywords = ['ethics', 'moral', 'right', 'wrong', 'good', 'bad', 'justice', 'fairness', 'equality', 'responsibility']
edu_keywords = ['education', 'learning', 'teaching', 'school', 'university', 'student', 'teacher', 'curriculum', 'knowledge', 'skill']

def calculate_keyword_score(text, keywords):
    """
    Calculate a score based on the frequency of keywords in the text.
    """
    words = word_tokenize(text.lower())
    word_freq = Counter(words)
    
    score = sum(word_freq[keyword.lower()] for keyword in keywords if keyword.lower() in word_freq)
    
    # Normalize the score by the total number of words
    total_words = len(words)
    if total_words > 0:
        normalized_score = score / total_words
    else:
        normalized_score = 0
    
    return normalized_score

# Example usage
if __name__ == "__main__":
    sample_text = "Artificial Intelligence and machine learning are revolutionizing various industries, raising important ethical considerations."
    
    tech_score = calculate_keyword_score(sample_text, tech_keywords)
    ethics_score = calculate_keyword_score(sample_text, ethics_keywords)
    edu_score = calculate_keyword_score(sample_text, edu_keywords)
    
    print(f"Technology Score: {tech_score:.4f}")
    print(f"Ethics Score: {ethics_score:.4f}")
    print(f"Education Score: {edu_score:.4f}")
