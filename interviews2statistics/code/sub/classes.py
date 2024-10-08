import re
from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import simple_preprocess

class Contribution:
    def __init__(self, text: str):
        self.text = text
        self.word_count = len(re.findall(r'\w+', text))
        self.processed_text = [word for word in simple_preprocess(text) if word not in STOPWORDS]

class Discussion:
    def __init__(self):
        self.contributions = []

    def add_contribution(self, text: str):
        self.contributions.append(Contribution(text))