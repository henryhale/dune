import nltk

def init():
    """
    Initialize environment - download required data
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
