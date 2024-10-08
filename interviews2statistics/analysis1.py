# File: code/sub/analysis1.py

import numpy as np
import re
from gensim import corpora
from gensim.models import LdaModel
from gensim.parsing.preprocessing import STOPWORDS
from typing import List, Dict, Tuple, Set
from collections import Counter
from .classes import Contribution, Discussion

# Keyword sets
tech_keywords = set([
    '3d printing', '5g', 'additive manufacturing', 'ai', 'algorithm', 'analytics', 'api', 'ar',
    'artificial intelligence','attack' ,'attribute', 'augmented reality', 'automate', 'automating', 'automation',
    'autonomous vehicle', 'aws', 'azure', 'backend', 'bash', 'bias', 'big data', 'biometrics','brain'
    'blockchain', 'bot', 'calculus', 'c++', 'cad', 'chat', 'chatbot', 'chip', 'classification',
    'classifier', 'cloud computing', 'clustering', 'code', 'coding','cognitive', 'compute', 'computer',
    'computer vision', 'computer-aided design', 'computing', 'context window', 'conversation',
    'cpu', 'cryptocurrency', 'cybersecurity', 'data', 'data analysis', 'data mining', 'data science',
    'data visualization', 'deep learning', 'descriptive', 'devops', 'digital', 'digital twin',
    'digitalization', 'digitization', 'document', 'docker', 'edge computing', 'enabled', 'engine',
    'explainable ai', 'feature', 'gan', 'generative', 'generative adversarial network', 'github',
    'gpu', 'hardware', 'image', 'innovation', 'internet', 'internet of things', 'iot', 'java',
    'javascript', 'kaggle', 'kubernetes', 'large language model', 'layer', 'library', 'libraries',
    'linear algebra', 'linguistic', 'linguistics', 'lora', 'machine learning', 'mathematics',
    'mathplotlib', 'metaverse', 'method', 'microservices', 'model', 'multilingual', 'natural language',
    'natural language processing', 'network', 'neural network', 'nft', 'nlp', 'nltk', 'numpy',
    'nvidia', 'pandas', 'parameter', 'parameter tuning', 'predictive', 'processing', 'processor',
    'programming', 'python', 'pytorch', 'quantum computing', 'r','real-time','reinforcement learning',
    'regression', 'research', 'robotics', 'scikit-learn', 'scipy', 'script', 'security', 'seaborn',
    'semantics', 'server', 'serverless', 'smart contract', 'smart device', 'software', 'spacy', 'sql',
    'statistical', 'statistics', 'supervised', 'syntax', 'tableau', 'task', 'technical', 'technologies',
    'technology', 'telemedicin', 'telemedicine', 'tensorflow', 'text','threat' ,'tool', 'trained', 'transfer learning',
    'translation', 'unsupervised', 'user experience', 'UX', 'virtual', 'virtual reality', 'visualize',
    'visualization', 'voice', 'vr', 'web development', 'web3', 'weight', 'augmented reality', 'mixed reality',
    'edge computing', 'serverless', 'microservices', 'container', 'docker', 'kubernetes', 'data mining',
    'data visualization', 'smart contract', 'cryptocurrency', 'nft', 'web3', 'metaverse', 'digital twin',
    'computer-aided design', 'cad', '3d printing', 'additive manufacturing', 'internet of things',
    'natural language processing', 'user experience','UX'
])


edu_keywords = set([
    'adaptive assessment', 'adaptive learning', 'ai-powered tutoring', 'artificial intelligence in education',
    'asynchronous learning', 'augmented reality in education', 'automated grading', 'blended learning',
    'collaborative learning', 'collaborative tools', 'competency-based education', 'data literacy',
    'digital assessment', 'digital badges', 'digital literacy', 'digital storytelling', 'distance education',
    'e-learning', 'e-portfolio', 'educational data mining', 'educational technology', 'edtech', 'flipped classroom',
    'game-based learning', 'gamification', 'immersive learning', 'information literacy', 'interactive content',
    'learning analytics', 'learning experience platform', 'learning management system', 'lms', 'media literacy',
    'microlearning', 'mobile learning', 'm-learning', 'mooc', 'multimedia production', 'online course',
    'online proctoring', 'peer-to-peer learning', 'performance tracking', 'personalized learning',
    'podcasting', 'project management software', 'project-based learning', 'remote learning',
    'self-paced learning', 'simulation-based learning', 'social learning', 'synchronous learning',
    'video conferencing', 'video editing', 'video-based learning', 'virtual classroom', 'virtual reality in education',
    'virtual tutoring', 'digital whiteboards', 'file sharing platforms', 'graphic design', 'lxp',
    'massive open online course', 'serious games', 'digital assessment', 'e-portfolio', 'digital badges',
    'learning analytics', 'educational data mining', 'artificial intelligence in education', 'virtual tutoring',
    'adaptive assessment', 'immersive learning', 'simulation-based learning', 'augmented reality in education',
    'virtual reality in education', 'game-based learning', 'digital storytelling', 'online proctoring',
    'remote learning', 'distance education', 'synchronous learning', 'asynchronous learning',
    'video-based learning', 'interactive content', 'learning experience platform', 'lxp', 'massive open online course',
    'collaborative tools', 'project management software', 'video conferencing', 'digital whiteboards',
    'file sharing platforms', 'multimedia production', 'podcasting', 'video editing', 'graphic design',
    'serious games', 'performance tracking', 'ai-powered tutoring', 'automated grading'
])


ethics_keywords = set([
    'accessibility', 'accountability', 'algorithmic accountability', 'algorithmic bias', 'algorithmic transparency',
    'ai governance', 'ai safety', 'assistive technologies', 'automation ethics', 'bias detection',
    'content moderation', 'copyright', 'cyberbullying prevention', 'cybersecurity ethics', 'data anonymization',
    'data minimization', 'data privacy', 'data protection', 'data sovereignty', 'digital addiction',
    'digital citizenship', 'digital detox', 'digital divide', 'digital empowerment', 'digital ethics',
    'digital identity', 'digital inclusion', 'digital labor rights', 'digital literacy', 'digital rights',
    'digital rights management', 'digital well-being', 'disinformation', 'e-waste', 'energy-efficient technologies',
    'ergonomics', 'ethical ai', 'ethical hacking', 'ethical sourcing', 'explainable ai', 'fair use',
    'fairness', 'fairness in ai', 'gdpr', 'green computing', 'human-ai collaboration', 'inclusive design',
    'inclusive digital practices', 'information ethics', 'information security policies', 'informed consent',
    'intellectual property', 'misinformation', 'net neutrality', 'online harassment', 'online safety',
    'open source', 'open-source licensing', 'privacy by design', 'responsible ai', 'responsible disclosure',
    'responsible innovation', 'right to be forgotten', 'screen time management', 'sustainability',
    'sustainable it practices', 'tech addiction', 'tech for good', 'transparency', 'universal design',
    'web accessibility standards', 'digital rights management', 'information security policies',
    'energy-efficient technologies', 'sustainable it practices', 'screen time management', 'digital detox',
    'ergonomics', 'cyberbullying prevention', 'human-ai collaboration', 'automation ethics'
])

def preprocess_text(text: str) -> str:
    # Convert to lowercase and remove punctuation
    text = re.sub(r'[^\w\s]', '', text.lower())
    return text

def find_keyword_matches(text: str, keywords: Set[str], count_multiple: bool) -> List[str]:
    text = preprocess_text(text)
    if count_multiple:
        return [keyword for keyword in keywords if keyword in text]
    else:
        return list(set(keyword for keyword in keywords if keyword in text))

def calculate_keyword_score(text: str, keywords: Set[str], count_multiple: bool) -> Tuple[float, List[str]]:
    processed_text = preprocess_text(text)
    matches = find_keyword_matches(processed_text, keywords, count_multiple)
    score = len(matches) / len(processed_text.split()) if processed_text else 0
    return score, matches

def remove_stopwords(text: str) -> List[str]:
    if not text:
        return []
    return [word.lower() for word in text.split() if word.lower() not in STOPWORDS]


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

def analyze_interview(filename: str, contributions: List[Tuple[int, Contribution]], config: Dict) -> List[Dict]:
    print(f"\n{'='*50}")
    print(f"Analyzing interview: {filename}")
    print(f"{'='*50}")
    results = []
    
    count_multiple = config.get('count_multiple_keywords', False)
    
    for iteration, contrib in contributions:
        print(f"\n{'-'*50}")
        print(f"Document: {filename}, Iteration: {iteration}")
        print(f"{'-'*50}")

        if not contrib.text:
            print("No text to analyze.")
            continue

        tech_score, tech_matches = calculate_keyword_score(contrib.text, tech_keywords, count_multiple)
        ethics_score, ethics_matches = calculate_keyword_score(contrib.text, ethics_keywords, count_multiple)
        education_score, education_matches = calculate_keyword_score(contrib.text, edu_keywords, count_multiple)

        print("Matching Score Words:")
        print(f"  Technology ({tech_score:.4f}): {', '.join(tech_matches)}")
        print(f"  Ethics ({ethics_score:.4f}): {', '.join(ethics_matches)}")
        print(f"  Education ({education_score:.4f}): {', '.join(education_matches)}")
        
        print(f"Total words in processed text: {len(contrib.text.split())}")

        results.append({
            "filename": filename,
            "iteration": iteration,
            "tech_score": tech_score,
            "tech_matches": tech_matches,
            "ethics_score": ethics_score,
            "ethics_matches": ethics_matches,
            "education_score": education_score,
            "education_matches": education_matches
        })

    print(f"\nAnalysis complete for: {filename}")
    return results

def analyze_keyword_frequency(text: str, top_n: int = 10):
    # (Keep this function as it was)

    # Print the keyword sets to ensure they're not empty
    print("Tech keywords:", tech_keywords)
    print("Ethics keywords:", ethics_keywords)
    print("Education keywords:", edu_keywords)