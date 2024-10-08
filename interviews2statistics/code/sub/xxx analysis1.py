import numpy as np
from gensim import corpora
from gensim.models import LdaModel
from gensim.parsing.preprocessing import STOPWORDS
from typing import List, Dict, Tuple
from collections import Counter
from .classes import Contribution, Discussion

# Keyword sets
tech_keywords = set([
    'ai', 'algorithm', 'analytics', 'api', 'artificial intelligence', 'attribute', 'automate', 'automating',
    'automation', 'autonomous vehicle', 'aws', 'azure', 'backend', 'bash', 'bias', 'big data', 'biometrics',
    'blockchain', 'bot', 'calculus', 'c++', 'chat', 'chatbot', 'chip', 'classification', 'classifier',
    'cloud computing', 'clustering', 'code', 'computer', 'computer vision', 'computing', 'context window',
    'conversational', 'cybersecurity', 'data', 'data analysis', 'data analytics','data science', 'deep learning', 'descriptive',
    'devops', 'digital', 'digitalization', 'digitization', 'document', 'enabled', 'engine',
    'explainable ai', 'feature', 'gan', 'generative', 'generative adversarial network', 'github', 'gpu',
    'hardware', 'image', 'innovation', 'internet', 'iot', 'java', 'javascript', 'kaggle', 'large language model',
    'layer', 'llm', 'library', 'libraries', 'linear algebra', 'linguistic', 'linguistics', 'lora', 'machine learning',
    'mathematics', 'mathplotlib', 'method', 'model', 'multilingual', 'natural language', 'network', 'neural network',
    'nlp', 'nltk', 'numpy', 'pandas', 'parameter', 'parameter tuning', 'predictive', 'processing', 'processor', 'programming', 'python',
    'pytorch', 'quantum computing', 'r', 'reinforcement learning', 'regression', 'research', 'robotics', 'seaborn',
    'scikit-learn', 'scipy', 'script', 'security', 'semantics', 'server', 'speech', 'statistical', 'statistics',
    'smart device', 'software', 'spacy', 'sql', 'supervised', 'syntax', 'tableau', 'task', 'technical',
    'technologies', 'technology', 'text', 'tensorflow', 'tool', 'trained', 'transfer learning', 'translation',
    'unsupervised', 'virtual reality', 'visualize', 'visualization', 'virtual', 'vr', 'web development',
    'voice', 'weight'
])

ethics_keywords = set([
    'accountability', 'accountable', 'authenticate', 'authentication', 'bias', 'concern', 'considerate',
    'considerations', 'data breach', 'deceptive', 'dilemma', 'discriminatory', 'discrimination', 'ethicist', 'ethics',
    'ethical', 'fair', 'fairness', 'fraudulent', 'guideline', 'hack', 'harm', 'harmful', 'inclusion', 'inclusive',
    'inclusivity', 'law', 'liable', 'liability', 'manipulative', 'moral', 'policymaker', 'privacy', 'protect', 'protection',
    'regulate', 'regulation', 'regulatory', 'responsibility', 'risk', 'risks', 'risky', 'safe', 'safety', 'secure',
    'security', 'societal', 'society', 'transparency', 'transparent', 'unfair', 'vulnerabilities', 'vulnerability'
])

edu_keywords = set([
    'collaborate', 'competence', 'competent', 'continuous learning', 'course', 'education', 'enroll', 'experience',
    'hands-on', 'informed', 'insight', 'interdisciplinary', 'lab', 'learner', 'learning style', 'master', 'phd',
    'proficiency', 'proficient', 'project', 'self-study', 'skill', 'teamwork', 'training', 'understand', 'upskill'
])

def remove_stopwords(text: str) -> List[str]:
    if not text:
        return []
    return [word for word in text.lower().split() if word not in STOPWORDS]

def perform_topic_modeling(contributions: List[Contribution], num_topics: int = None):
    if not contributions:
        return []

    texts = [remove_stopwords(contrib.text) for contrib in contributions]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    if not corpus:
        return []

    if num_topics is None:
        num_topics = max(1, min(10, len(corpus) // 2))

    try:
        lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, passes=15)
    except ValueError as e:
        print(f"Error in LDA model creation: {e}")
        return []

    topics = []
    for topic_id in range(num_topics):
        topics.append(dict(lda_model.show_topic(topic_id, topn=10)))

    return topics

def calculate_keyword_score(text: List[str], keywords: set) -> float:
    keyword_count = sum(1 for word in text if word.lower() in keywords)
    return keyword_count / len(text) if text else 0

def analyze_interview(filename: str, contributions: List[Tuple[int, Contribution]]) -> List[Dict]:
    print(f"Analyzing interview: {filename}")
    results = []

    for iteration, contrib in contributions:
        print(f"\nAnalyzing document: {filename}, Iteration: {iteration}")

        if not contrib.text:
            print("No summary text to analyze.")
            continue

        processed_text = contrib.text.lower().split()
        tech_score = calculate_keyword_score(processed_text, tech_keywords)
        ethics_score = calculate_keyword_score(processed_text, ethics_keywords)
        education_score = calculate_keyword_score(processed_text, edu_keywords)

        print(f"Scores for {filename}, Iteration {iteration}:")
        print(f"Technology Score: {tech_score:.4f}")
        print(f"Ethics Score: {ethics_score:.4f}")
        print(f"Education Score: {education_score:.4f}")

        print(f"Number of words in processed text: {len(processed_text)}")
        print(f"Number of tech keywords found: {sum(1 for word in processed_text if word in tech_keywords)}")
        print(f"Number of ethics keywords found: {sum(1 for word in processed_text if word in ethics_keywords)}")
        print(f"Number of education keywords found: {sum(1 for word in processed_text if word in edu_keywords)}")

        results.append({
            "filename": filename,
            "iteration": iteration,
            "tech_score": tech_score,
            "ethics_score": ethics_score,
            "education_score": education_score
        })

    print(f"Analysis complete for: {filename}")
    return results

# Print the keyword sets to ensure they're not empty
print("Tech keywords:", tech_keywords)
print("Ethics keywords:", ethics_keywords)
print("Education keywords:", edu_keywords)

def analyze_keyword_frequency(text: str, top_n: int = 10):
    words = remove_stopwords(text)
    if not words:
        return []
    word_freq = Counter(words)
    return word_freq.most_common(top_n)

# Also, let's print the keyword sets to ensure they're not empty
#print("Tech keywords:", tech_keywords)
#print("Ethics keywords:", ethics_keywords)
#print("Education keywords:", edu_keywords)
