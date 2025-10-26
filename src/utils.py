"""
Utility functions for data handling and text preprocessing 
"""

import pandas
import joblib
import pathlib
import nltk
import numpy
import random
import os

# added these for reproducibility on different machines
numpy.random.seed(42)
random.seed(42)
os.environ['PYTHONHASHSEED'] = '0'


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
    df = pandas.read_csv(filepath, encoding='utf-8')
    df =  df.sort_values('label').reset_index(drop=True)

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
