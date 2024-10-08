import numpy as np
from gensim import corpora
from gensim.models import LdaModel
from gensim.parsing.preprocessing import STOPWORDS
from typing import List
from collections import Counter
from .classes import Contribution, Discussion

# Extended tech keywords list
tech_keywords = set([
    'ai', 'algorithm', 'analytics', 'api', 'automation', 'backend', 'big data', 'biometrics',
    'blockchain', 'bot', 'chat', 'chip', 'classification', 'classifier', 'cloud', 'code',
    'computer', 'computing', 'cybersecurity', 'data', 'deep learning', 'devops', 'digital',
    'encryption', 'engine', 'hardware', 'internet', 'iot', 'java', 'javascript', 'large language model',
    'llm', 'machine learning', 'network', 'neural network', 'processor', 'programming', 'python',
    'quantum computing', 'robotics', 'script', 'security', 'server', 'statistics', 'smart devices',
    'software', 'technology', 'virtual reality', 'vr', 'web development'
])

def remove_stopwords(text: str) -> List[str]:
    return [word for word in text.lower().split() if word not in STOPWORDS]

def calculate_tech_orientation(contributions: List[Contribution], num_topics: int = None):
    if not contributions:
        return [], [], []

    texts = [remove_stopwords(contrib.text) for contrib in contributions]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    if not corpus:
        return [], [], []

    # Determine number of topics based on corpus size
    if num_topics is None:
        num_topics = max(1, min(10, len(corpus) // 2))

    try:
        lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, passes=15)
    except ValueError as e:
        print(f"Error in LDA model creation: {e}")
        return [], [], []

    topic_tech_scores = []
    topic_words = []
    for topic_id in range(num_topics):
        words = dict(lda_model.show_topic(topic_id, topn=10))
        topic_words.append(list(words.keys()))
        tech_word_count = sum(1 for word in words if word in tech_keywords)
        tech_score = tech_word_count / len(words)
        topic_tech_scores.append(tech_score)

    contrib_tech_scores = []
    for bow in corpus:
        topic_dist = lda_model.get_document_topics(bow)
        tech_score = sum(score * topic_tech_scores[topic_id] for topic_id, score in topic_dist)
        contrib_tech_scores.append(tech_score)

    return topic_tech_scores, contrib_tech_scores, topic_words

def analyze_keyword_frequency(text: str, top_n: int = 10):
    words = remove_stopwords(text)
    word_freq = Counter(words)
    return word_freq.most_common(top_n)

def calculate_readability(text: str):
    sentences = text.split('.')
    words = text.split()
    avg_sentence_length = len(words) / len(sentences)
    return avg_sentence_length

def analyze_discussion(discussion: Discussion):
    print(f"\nAnalyzing document with {len(discussion.contributions)} text")
    
    if not discussion.contributions:
        print("No text to analyze.")
        return

    topic_tech_scores, contrib_tech_scores, topic_words = calculate_tech_orientation(discussion.contributions)

    if topic_tech_scores:
        print("\nTopic Technology Orientation:")
        for i, (score, words) in enumerate(zip(topic_tech_scores, topic_words)):
            print(f"Topic {i+1} ({', '.join(words[:5])}): {score:.4f}")

    if contrib_tech_scores:
        print("\nText Technology Orientation:")
        for i, score in enumerate(contrib_tech_scores):
            print(f"Text {i+1}: {score:.4f}")

        print(f"\nOverall Technology Orientation: {np.mean(contrib_tech_scores):.4f}")
    else:
        print("Unable to calculate technology orientation.")

    # Additional analysis
    full_text = ' '.join([contrib.text for contrib in discussion.contributions])
    
    print("\nTop 10 Most Frequent Words (excluding stop words):")
    for word, count in analyze_keyword_frequency(full_text):
        print(f"{word}: {count}")

    readability_score = calculate_readability(full_text)
    print(f"\nReadability Score (Avg. Sentence Length): {readability_score:.2f}")

    for i, contrib in enumerate(discussion.contributions):
        print(f"\nText {i+1} start: {' '.join(remove_stopwords(contrib.text)[:20])}...")