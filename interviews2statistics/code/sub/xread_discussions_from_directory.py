import math
import re
from typing import List, Callable
from gensim import corpora
from gensim.models import LdaModel
from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import simple_preprocess
import numpy as np

class Contribution:
    def __init__(self, text: str):
        self.text = text
        self.word_count = len(re.findall(r'\w+', text))
        self.processed_text = [word for word in simple_preprocess(text) if word not in STOPWORDS]

class Discussion:
    def __init__(self):
        self.contributions: List[Contribution] = []

    def add_contribution(self, text: str):
        self.contributions.append(Contribution(text))

    def get_total_words(self) -> int:
        return sum(contrib.word_count for contrib in self.contributions)

def calculate_normalized_entropy(contributions: List[Contribution]) -> float:
    word_counts = [contrib.word_count for contrib in contributions]
    total_words = sum(word_counts)
    proportions = [count / total_words for count in word_counts]
    entropy = -sum(p * math.log2(p) for p in proportions if p > 0)
    max_entropy = math.log2(len(contributions))
    return entropy / max_entropy if max_entropy > 0 else 0

def calculate_topic_diversity(contributions: List[Contribution], num_topics: int = 5) -> float:
    if len(contributions) < 2:
        return 0  # Not enough contributions for meaningful topic diversity

    dictionary = corpora.Dictionary([contrib.processed_text for contrib in contributions])
    corpus = [dictionary.doc2bow(contrib.processed_text) for contrib in contributions]
    
    try:
        lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, passes=10)
        topic_distributions = lda_model.get_document_topics(corpus, minimum_probability=0)
        
        # Calculate Jensen-Shannon divergence between topic distributions
        js_divergences = []
        for i in range(len(topic_distributions)):
            for j in range(i+1, len(topic_distributions)):
                dist1 = dict(topic_distributions[i])
                dist2 = dict(topic_distributions[j])
                js_div = jensen_shannon_divergence(dist1, dist2)
                js_divergences.append(js_div)
        
        return np.mean(js_divergences) if js_divergences else 0
    except Exception as e:
        print(f"Error in topic modeling: {e}")
        return 0

def jensen_shannon_divergence(dist1, dist2):
    # Ensure all topics are present in both distributions
    all_topics = set(dist1.keys()) | set(dist2.keys())
    dist1 = {topic: dist1.get(topic, 0) for topic in all_topics}
    dist2 = {topic: dist2.get(topic, 0) for topic in all_topics}
    
    # Calculate mean distribution
    m = {topic: (dist1[topic] + dist2[topic]) / 2 for topic in all_topics}
    
    # Calculate KL divergences
    kl_d1m = sum(dist1[topic] * math.log2(dist1[topic] / m[topic]) for topic in all_topics if dist1[topic] > 0)
    kl_d2m = sum(dist2[topic] * math.log2(dist2[topic] / m[topic]) for topic in all_topics if dist2[topic] > 0)
    
    # Calculate Jensen-Shannon divergence
    return (kl_d1m + kl_d2m) / 2

def read_discussion_from_file(file_path: str) -> Discussion:
    discussion = Discussion()
    with open(file_path, 'r') as file:
        current_contribution = ""
        for line in file:
            if line.strip().startswith("Contribution"):
                if current_contribution:
                    discussion.add_contribution(current_contribution.strip())
                current_contribution = ""
            else:
                current_contribution += line
        if current_contribution:
            discussion.add_contribution(current_contribution.strip())
    return discussion

def main():
    file_path = "/Users/dietmar/Dropbox/PycharmProjects/MyPersonaFlex/data/outputs/focus_group_results.txt"
    discussion = read_discussion_from_file(file_path)

    print("Incremental Normalized Entropy Calculation:")
    for i in range(1, len(discussion.contributions) + 1):
        partial_discussion = Discussion()
        partial_discussion.contributions = discussion.contributions[:i]
        entropy = calculate_normalized_entropy(partial_discussion.contributions)
        print(f"After {i} contribution(s): {entropy:.4f}")

    print("\nOverall Normalized Entropy:")
    overall_entropy = calculate_normalized_entropy(discussion.contributions)
    print(f"Total normalized entropy: {overall_entropy:.4f}")

    print("\nTopic Diversity:")
    topic_diversity = calculate_topic_diversity(discussion.contributions)
    print(f"Topic diversity: {topic_diversity:.4f}")

    # Simulate adding a new contribution
    new_contribution = "This is a new contribution with about 20 words to test the entropy calculation after adding it to the discussion."
    discussion.add_contribution(new_contribution)

    print("\nAfter adding new contribution:")
    new_entropy = calculate_normalized_entropy(discussion.contributions)
    print(f"New overall normalized entropy: {new_entropy:.4f}")
    print(f"Normalized entropy change: {new_entropy - overall_entropy:.4f}")

    new_topic_diversity = calculate_topic_diversity(discussion.contributions)
    print(f"New topic diversity: {new_topic_diversity:.4f}")
    print(f"Topic diversity change: {new_topic_diversity - topic_diversity:.4f}")

if __name__ == "__main__":
    main()