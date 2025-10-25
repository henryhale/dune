from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.preprocessing import LabelEncoder
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import os
import re
import pandas


stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def clean_text(text):
    """
    Clean text input - preparing it for vectorization & reduce noise
    - tokenization
    - lowercasing
    - stopword removal
    """
    # convert all text to lowercase
    text = text.lower()
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

    return " ".join(tokens)


def preprocess(df: pandas.DataFrame):
    """
    Preprocesses the dataset by cleaning the `text` and encoding the `labels`
    """
    # clean features - text
    df["cleaned_text"] = df["text"].apply(clean_text)

    # encode labels
    label_encoder = LabelEncoder()
    df["encoded_label"] = label_encoder.fit_transform(df["label"])

    return label_encoder
