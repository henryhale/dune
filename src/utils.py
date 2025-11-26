"""
Utility functions for data handling and text preprocessing 
"""

import pandas
import joblib
import os
import pathlib
import nltk
import numpy
import random
import re
import unicodedata
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# added these for reproducibility on different machines
numpy.random.seed(42)
random.seed(42)
os.environ["PYTHONHASHSEED"] = "0"


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


def check_nltk_data():
    """
    Initialize environment - download required NLTK data
    """
    # check if necessary nltk data exists otherwise download
    nltk_data = [
        {"package": "corpora/stopwords", "name": "stopwords"},
        {"package": "tokenizers/punkt", "name": "punkt"},
        {"package": "corpora/wordnet", "name": "wordnet"},
        {"package": "corpora/omw-1.4", "name": "omw-1.4"},
        {"package": "punkt_tab", "name": "punkt_tab"},
    ]

    for data in nltk_data:
        try:
            nltk.data.find(data["package"])
        except LookupError:
            nltk.download(data["name"])


def load_dataset(filepath):
    """
    Load dataset from CSV file

    Args:
        filepath (str): Path to CSV dataset file

    Returns:
        list: List of (text, label) tuples
    """
    df = pandas.read_csv(filepath, encoding="utf-8")
    df = df.sort_values("label").reset_index(drop=True)

    return list(zip(df["text"], df["label"]))


def save_dataset(dataset, filepath):
    """
    Save dataset to CSV file

    Args:
        dataset (list): List of (text, label) tuples
        filepath (str): Output path for CSV file
    """
    pathlib.Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    df = pandas.DataFrame(dataset, columns=["text", "label"])
    df.to_csv(filepath, index=False)


def save_model(model, filepath, compress=True):
    """
    Save model to disk using joblib

    Args:
        model: Model object to save
        filepath (str): Output path for model file. The compression method corresponding to one of the supported filename extensions ('.z', '.gz', '.bz2', '.xz' or '.lzma') will be used automatically.
        compress: If compress is a 2-tuple, the first element must correspond to a string between supported compressors (e.g 'zlib', 'gzip', 'bz2', 'lzma' 'xz'), the second element must be an integer from 0 to 9, corresponding to the compression level.
    """
    pathlib.Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "wb") as file:
        joblib.dump(model, file, compress)


def load_model(filepath):
    """
    Load model from disk

    Args:
        filepath (str): Path to model file
    """
    with open(filepath, "rb") as file:
        return joblib.load(file)


def generate_onnx_model(filepath, pipeline=None):
    """
    Convert a .joblib model to ONNX format

    Args:
        filepath (str): Path to a .joblib model
    """
    
    from skl2onnx import convert_sklearn
    from skl2onnx.common.data_types import StringTensorType

    model = None
    if pipeline is not None:
        model = pipeline
    else:
        model = joblib.load(filepath)
    # print(model)
    onnx_model = convert_sklearn(
        model,
        initial_types=[("input", StringTensorType([None, 1]))],
        options={"classifier": {"output_class_labels": False}},
    )
    filepath = filepath.replace("joblib", "onnx")
    with open(filepath, "wb") as file:
        file.write(onnx_model.SerializeToString())
