"""
Preprocess input text to eliminate noise like punctuation, extra spaces, and stop words
"""

import os
import pandas
import argparse
from src.train import split_data
from src.utils import clean_text, check_nltk_data 

def prepare_data(test_size=0.2, verbose=False):
    # download nltk data
    check_nltk_data()

    # merge all csv files into one dataset file
    df = pandas.DataFrame()

    for root, dirs, files in os.walk("./data/"):
        for file in files:
            if verbose:
                print(f"checking: {file}")
            filepath = os.path.join(root, file)
            if filepath.lower().endswith(".csv") and file != "dataset.csv":
                tmp_df = pandas.read_csv(filepath)
                if verbose:
                    print(f"{filepath}: {tmp_df.shape}")
                df = pandas.concat([df, tmp_df], ignore_index=True)

    df.to_csv("./data/dataset.csv", index=None)

    # clean text
    df["cleaned_text"] = df["text"].apply(clean_text)

    # split the dataset
    x_train, x_test, y_train, y_test = split_data(
        x=df["cleaned_text"], y=df["label"], test_size=test_size
    )

    traindf = pandas.DataFrame()
    traindf["text"] = x_train
    traindf["label"] = y_train
    traindf.to_csv("./data/dataset.training.csv", index=None)

    testdf = pandas.DataFrame()
    testdf["text"] = x_test
    testdf["label"] = y_test
    testdf.to_csv("./data/dataset.testing.csv", index=None)


def main():
    """
    A command line inteface for data preprocessing
    """
    parser = argparse.ArgumentParser(description="CLI for data preprocessing")
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Proportion of the data for validation set (default: 0.2)",
    )
    parser.add_argument(
        "--verbose",
        type=bool,
        default=False,
        help="Whether or not to display more details",
    )

    args = parser.parse_args()

    print("[dune]: preparing data...")
    prepare_data(test_size=args.test_size, verbose=args.verbose)
    print("[dune]: preprocessing complete!")


if __name__ == "__main__":
    main()
