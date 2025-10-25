"""
Data augmentation using custom fillers and NLTK synonym replacement
"""

import argparse
import random
import nltk
from nltk.corpus import wordnet
from utils import load_dataset, save_dataset


def synonym_augment(text, num_replacements=2):
    """
    Augment text by replacing known words with alternatives - synonyms

    Args:
        text (str): Input text to operate on
        num_replacements (int): Number of replacements to make in the text

    Returns:
        str: Augmented text
    """
    try:
        nltk.data.find("corpora/wordnet")
    except LookupError:
        nltk.download("wordnet")

    words = text.split()
    for _ in range(num_replacements):
        idx = random.randint(0, len(words) - 1)
        word = words[idx]
        synsets = wordnet.synsets(word)
        if synsets:
            synonym = random.choice(synsets).lemmas()[0].name().replace("_", " ")
            words[idx] = synonym
    return " ".join(words)


def add_filler_words(text):
    """
    Add filler word at the beginning

    Args:
        text (str): Input text

    Returns:
        str: Text with a filler added
    """
    fillers = ["please", "can you", "hi", "hey", "hello", "can you", "could you", ""]
    random_filler = random.choice(fillers)
    return random_filler + (" " if random_filler else "") + text


def augment_sample(text, label, num_variations=5):
    """
    Generate multiple vairations of a single sample

    Args:
        text (str): Input text to augment
        label (str): Label or output class
        num_variations (int): Number of variations to  create

    Returns:
        list: List of (text, label) tuples
    """
    variations = [(text, label)]
    for _ in range(num_variations):
        augmented = text

        # 50% chance of synonym replacement
        if random.random() > 0.5:
            augmented = synonym_augment(text, num_replacements=random.randint(1, 2))

        # 30% chance of adding a filler
        if random.random() > 0.7:
            augmented = add_filler_words(augmented)

        if augmented != text:
            variations.append((augmented, label))

    return variations


def augment_dataset(input_path, output_path, multiplier=5):
    """
    Augment the entire dataset

    Args:
        input_path (str): Path to input(original) dataset
        output_path (str): Path to output(augmented) dataset
        multiplier (int): How many variations per sample

    Returns:
        int: Total number of samples in augmented dataset
    """
    dataset = load_dataset(input_path)

    augmented_dataset = []

    for text, label in dataset:
        variations = augment_sample(text, label, multiplier)
        augmented_dataset.extend(variations)

    save_dataset(augmented_dataset, output_path)

    return len(augmented_dataset)


def main():
    """
    A command line interface for data augmentation
    """
    parser = argparse.ArgumentParser(description="Augment training dataset")
    parser.add_argument(
        "--input",
        type=str,
        default="data/dataset.csv",
        help="Path to original dataset file in CSV format",
    )
    parser.add_argument(
        "---output",
        type=str,
        default="data/dataset.augmented.csv",
        help="Path to which the augmented dataset file will be saved",
    )
    parser.add_argument(
        "--multiplier", type=int, default=5, help="Number of variations per sample"
    )

    args = parser.parse_args()

    print("[dune]: augmenting dataset...")

    n = augment_dataset(args.input, args.output, args.multiplier)

    print(f"[dune]: augmentation complete - {n} samples")


if __name__ == "__main__":
    main()
