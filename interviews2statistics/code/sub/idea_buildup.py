# sub/idea_buildup.py

import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# Initialize lemmatizer and stop words
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Preprocess each sentence
    processed_sentences = []
    for sentence in sentences:
        # Tokenize words, convert to lowercase, remove stopwords and punctuation, and lemmatize
        words = [lemmatizer.lemmatize(word.lower()) for word in nltk.word_tokenize(sentence)
                 if word.lower() not in stop_words and word.isalnum()]
        processed_sentences.append(' '.join(words))
    
    return processed_sentences

def calculate_idea_buildup(text):
    print("Calculating idea buildup...")
    # Preprocess the text
    processed_sentences = preprocess_text(text)
    
    # If there are fewer than 2 sentences, return 0 (no build-up)
    if len(processed_sentences) < 2:
        return 0
    
    # Create TF-IDF vectors for the sentences
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(processed_sentences)
    
    # Calculate cosine similarity between consecutive sentences
    similarities = []
    for i in range(len(processed_sentences) - 1):
        similarity = cosine_similarity(tfidf_matrix[i:i+1], tfidf_matrix[i+1:i+2])[0][0]
        similarities.append(similarity)
    
    # Calculate the average similarity as the idea build-up score
    idea_buildup_score = np.mean(similarities)
    
    print("Idea buildup calculation complete.")
    return idea_buildup_score

# Example usage
if __name__ == "__main__":
    sample_text = """
    Artificial Intelligence is revolutionizing various industries. 
    Machine learning, a subset of AI, is particularly impactful. 
    Deep learning, a technique in machine learning, has shown remarkable results in image and speech recognition. 
    These advancements are leading to new applications in healthcare, finance, and transportation.
    """
    
    score = calculate_idea_buildup(sample_text)
    print(f"Idea Build-up Score: {score:.4f}")
