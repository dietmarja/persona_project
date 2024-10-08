# sub/text_processing.py

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import nltk

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Get the set of stopwords
stop_words = set(stopwords.words('english'))

def remove_stopwords(text):
    """
    Remove stopwords from the given text.
    """
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word.lower() not in stop_words]
    return ' '.join(filtered_text)

def analyze_keyword_frequency(text, top_n=10):
    """
    Analyze the frequency of keywords in the given text.
    Returns the top N most frequent words (excluding stopwords).
    """
    word_tokens = word_tokenize(text.lower())
    filtered_words = [word for word in word_tokens if word not in stop_words and word.isalnum()]
    word_freq = Counter(filtered_words)
    return word_freq.most_common(top_n)

# Example usage
if __name__ == "__main__":
    sample_text = "Artificial Intelligence is revolutionizing various industries. Machine learning, a subset of AI, is particularly impactful."
    
    print("Original text:")
    print(sample_text)
    
    print("\nText with stopwords removed:")
    print(remove_stopwords(sample_text))
    
    print("\nTop 5 most frequent words:")
    for word, count in analyze_keyword_frequency(sample_text, top_n=5):
        print(f"{word}: {count}")
