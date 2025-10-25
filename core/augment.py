import random
import pandas
import nltk
from nltk.corpus import wordnet


def synonym_augment(text_str, num_replacements=2):
    """
    Augement data by replacing known words with alternatives - synonyms
    """
    try:
        nltk.data.find("corpora/wordnet")
    except LookupError:
        nltk.download("wordnet")

    words = text_str.split()
    for _ in range(num_replacements):
        idx = random.randint(0, len(words) - 1)
        word = words[idx]
        synsets = wordnet.synsets(word)
        if synsets:
            synonym = random.choice(synsets).lemmas()[0].name()
            words[idx] = synonym
    return " ".join(words)


def augment_data(df: pandas.DataFrame, variations=4, num_replacements=2):
    """
    Generate a new dataframe where each sample(row) is augumented `variations` times
    with `num_replacements` synonym changes.
    """
    augmented = []
    for i in range(df["text"].size):
        text = df["text"][i]
        label = df["label"][i]
        augmented.append((text, label))
        for _ in range(variations):  # generate n variations per sample
            augmented.append((synonym_augment(text, num_replacements), label))
    temp_df = pandas.DataFrame(augmented, columns=["text", "label"])
    return temp_df
