"""
Preprocess input text to eliminate noise like punctuation, extra spaces, and stop words
"""

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re
import unicodedata


stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def clean_text(text):
    """
    Clean text input to reduce noise and prepare it for vectorization
    - tokenization
    - lowercasing
    - stopword removal

    Args:
        text (str): User input text

    Returns:
        clean_text (str): Cleaned text with little noise
    """
    # convert all text to lowercase
    text = text.lower()
    # normalize text
    text = unicodedata.normalize("NFKD", text)
    # remove special characters and numbers to simplify vocabulary
    text = re.sub(r"[^a-z\s]", "", text)
    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()
    # break down text into individual words
    tokens = word_tokenize(text)
    # remove stopwords(irrelevant words like 'is', 'the', 'a')
    tokens = [word for word in tokens if word not in stop_words]
    # reduce words to their base or root form like 'running' to 'run'
    # this reduces vocabulary size and treat different inflections of a word as the same
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    result = " ".join(tokens)

    return text if len(result) == 0 else result
