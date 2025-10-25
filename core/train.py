import argparse
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    classification_report,
)
from utils import load_dataset, save_model
from preprocess import clean_text


def split_data(x, y, val_test_size=0.3, random_state=42):
    """
    Split the data into training and temp sets.
    The temp set is then split by half to create validation and testing sets.

    Args:
        x (list): List of input text data
        y (list): List of corresponding labels
        val_test_size (int): Percentage of validation and test set from entire dataset

    Returns:
        splitting: List containing train-val-test split of inputs.
    """

    # first split: train, temp (for validation/test)
    x_train, x_temp, y_train, y_temp = train_test_split(
        x, y, test_size=val_test_size, random_state=random_state, stratify=y
    )

    # second split: validation & test as 50/50 of temp
    x_val, x_test, y_val, y_test = train_test_split(
        x_temp, y_temp, test_size=0.5, random_state=random_state, stratify=y_temp
    )

    return x_train, x_val, x_test, y_train, y_val, y_test


def evaluate_set(y_true, y_pred, labels=None):
    """
    Evaluate the performance of the model basing on actual and predicted values

    Args:
        y_true (list): List of actual values
        y_pred (list): List of predicted values

    Returns:
        dict: An dictionary containing accuracy score and classification report
    """
    report = classification_report(
        y_true,
        y_pred,
        zero_division=0,
        target_names=labels,
    )

    accuracy = accuracy_score(y_true, y_pred)

    return {"accuracy": accuracy, "report": report}


def train_model(
    dataset_path,
    random_state=42,
    val_test_size=0.3,
    max_features=5000,
    ngram_range=(1, 3),
):
    """
    Trains text-to-command classification model

    Args:
        dataset_path (str): Path to dataset (CSV) file
        random_state (int): Random seed for reproducibility
        max_features (int): Maximum number of TF-IDF features
        ngram_range (tuple): Range of n-grams to extract

    Returns:
        tuple: (model, vectorizer, metrics)
    """
    # load dataset
    dataset = load_dataset(dataset_path)
    if not dataset:
        raise ValueError(f"[error]: no data found in {dataset_path}")

    # separate text and label columns
    texts = [item[0] for item in dataset]
    labels = [item[1] for item in dataset]

    # preprocess texts
    texts_cleaned = [clean_text(text) for text in texts]

    # encode labels
    encoder = LabelEncoder()
    labels_encoded = encoder.fit_transform(labels)

    # split data
    x_train, x_val, x_test, y_train, y_val, y_test = split_data(
        texts_cleaned, labels_encoded, val_test_size, random_state
    )

    # use `max_features` to limit features for efficiency
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        lowercase=True,
        strip_accents="unicode",
    )

    # initialize linear svc model
    model = LinearSVC(
        random_state=42, dual=False
    )  # dual=False for n_samples > n_features

    # fit and transform training data
    x_train_vec = vectorizer.fit_transform(x_train)

    # train model
    model.fit(x_train_vec, y_train)
    # training complete

    metrics = {}

    # evaluate on validation set
    x_val_vec = vectorizer.transform(x_val)
    y_val_pred = model.predict(x_val_vec)
    metrics["validation"] = evaluate_set(y_val, y_val_pred, encoder.classes_)

    # evaluate on testing set
    x_test_vec = vectorizer.transform(x_test)
    y_test_pred = model.predict(x_test_vec)
    metrics["testing"] = evaluate_set(y_test, y_test_pred, encoder.classes_)

    # save model and vectorizer
    save_model(vectorizer, "models/dune.vectorizer.joblib")
    save_model(model, "models/dune.model.joblib")

    return model, vectorizer, metrics


def main():
    """
    A command line inteface for model training
    """
    parser = argparse.ArgumentParser(
        description="CLI for text-to-command model training"
    )
    parser.add_argument(
        "--data",
        type=str,
        default="data/dataset.augmented.csv",
        help="Path to training data file (augmented or not) in CSV format",
    )
    parser.add_argument(
        "--val-test-size",
        type=float,
        default=0.3,
        help="Proportion of the data for both validation and test set (default: 0.3 - test 15%, validation 15%)",
    )
    parser.add_argument(
        "--max-features",
        type=int,
        default=5000,
        help="Maximum TF-IDF features (default: 5000)",
    )
    parser.add_argument(
        "--random-state", type=int, default=42, help="Random seed for reproducibility"
    )

    args = parser.parse_args()

    print("[dune]: training...")

    train_model(
        dataset_path=args.data,
        random_state=args.random_state,
        val_test_size=args.val_test_size,
        max_features=args.max_features,
    )

    print("[dune]: training complete")


if __name__ == "__main__":
    main()
