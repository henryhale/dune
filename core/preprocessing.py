from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import os
import re
import pandas


def validate_samples(data_dir, sample_size=100):
    """
    Combine all datasets into one csv file
    - Checks out each class specific dataset, validate and merge into one single dataset
    """
    df = pandas.DataFrame()

    size_dict = []

    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".csv") and "dataset" not in file:
                filepath = os.path.join(root, file)
                # print(f"found: {filepath}")
                tmp_df = pandas.read_csv(filepath)
                lines = len(tmp_df.input_variation)
                if lines != sample_size:
                    size_dict.append((filepath, lines))
                # print(f"merging... lines: {lines}")
                df = pandas.concat([df, tmp_df], ignore_index=True)
                # print(f"merged!")

    if len(size_dict) > 0:
        print("All classes must have the same number of samples.")
        print("The following need updating:")
        for f in size_dict:
            print(f"> {f[0]} - {f[1]}")
    else:
        print("All classes are valid.")
        # df.rename(columns={"input_variation": "text", "output_class": "label"})
        df.to_csv(os.path.join(data_dir, "dataset.csv"), index=None)


def clean_text(text):
    """
    Clean text input - preparing it for vectorization & reduce noise
    - tokenization
    - lowercasing
    - stopword removal
    """
    # change to lowercase
    text = text.lower()
    # remove punctuation, symbols and numbers
    text = re.sub(r"[^a-z\s]", "", text)
    # remove stop words
    tokens = [word for word in text.split() if word not in ENGLISH_STOP_WORDS]
    return " ".join(tokens)
