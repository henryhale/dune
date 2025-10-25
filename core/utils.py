"""
Utility functions for data handling and text preprocessing 
"""

import pandas
import joblib
import pathlib
import nltk


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
    df = pandas.read_csv(filepath)

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


def save_model(model, filepath):
    """
    Save model to disk using joblib

    Args:
        model: Model object to save
        filepath (str): Output path for model file
    """
    pathlib.Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "wb") as file:
        joblib.dump(model, file)


def load_model(filepath):
    """
    Load model from disk

    Args:
        filepath (str): Path to model file
    """
    with open(filepath, "rb") as file:
        return joblib.load(file)
