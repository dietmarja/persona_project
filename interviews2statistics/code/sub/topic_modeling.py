# sub/topic_modeling.py

from gensim import corpora
from gensim.models import LdaModel
from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import simple_preprocess

def perform_topic_modeling(contributions, num_topics=3, num_words=5):
    # Prepare the documents
    docs = [contribution.text for contribution in contributions]
    
    # Tokenize the documents
    texts = [[word for word in simple_preprocess(doc) if word not in STOPWORDS]
             for doc in docs]

    # Create a dictionary
    dictionary = corpora.Dictionary(texts)
    
    # Create a corpus
    corpus = [dictionary.doc2bow(text) for text in texts]
    
    # Train the LDA model
    lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)
    
    # Get the topics
    topics = lda_model.print_topics(num_words=num_words)
    
    # Convert topics to a more usable format
    topic_dict = {}
    for topic in topics:
        topic_id = topic[0]
        words = dict(word.split('*') for word in topic[1].split(' + '))
        topic_dict[topic_id] = words
    
    return topic_dict

# Example usage
if __name__ == "__main__":
    from collections import namedtuple
    Contribution = namedtuple('Contribution', ['text'])
    sample_contributions = [
        Contribution("Artificial Intelligence is revolutionizing various industries."),
        Contribution("Machine learning, a subset of AI, is particularly impactful."),
        Contribution("Deep learning has shown remarkable results in image recognition.")
    ]
    topics = perform_topic_modeling(sample_contributions)
    for topic_id, words in topics.items():
        print(f"Topic {topic_id + 1}: {', '.join(list(words.values())[:5])}")
