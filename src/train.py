import argparse
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    classification_report,
)
from src.utils import load_dataset, save_model
from src.preprocess import clean_text


def split_data(x, y, test_size=0.25, random_state=42):
    """
    Split the data into training and testing sets.

    Args:
        x (list): List of input text data
        y (list): List of corresponding labels
        test_size (int): Percentage of test set from entire dataset

    Returns:
        splitting: List containing train-val-test split of inputs.
    """
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
        shuffle=True,
    )

    return x_train, x_test, y_train, y_test


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
    pipeline_path="models/dune.pipeline.joblib.gz",
    random_state=42,
    test_size=0.15,
    max_features=5000,
    ngram_range=(1, 3),
):
    """
    Trains text-to-command classification model

    Args:
        dataset_path (str): Path to dataset (CSV) file
        pipeline_path (str): Path to which the model file will be saved
        random_state (int): Random seed for reproducibility
        max_features (int): Maximum number of TF-IDF features
        ngram_range (tuple): Range of n-grams to extract
        test_size (int): Percentage of test set from entire dataset

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

    # encode labels - nope sklearn internally encoded labels
    # encoded labels available at `model.classes_`
    # encoder = LabelEncoder()
    # labels_encoded = encoder.fit_transform(labels)

    # split data
    x_train, x_val, y_train, y_val = split_data(
        texts_cleaned, labels, test_size, random_state
    )

    # create pipeline for cleaner approach
    pipeline = Pipeline(
        [
            (
                "vectorizer",
                TfidfVectorizer(
                    max_features=max_features,
                    ngram_range=ngram_range,
                    lowercase=True,
                    strip_accents="unicode",
                ),
            ),
            (
                "classifier",
                LinearSVC(
                    max_iter=5000,
                    tol=1e-6,
                    loss="squared_hinge",
                    random_state=random_state,
                    dual=False,
                ),
            ),
        ]
    )

    # train pipeline
    pipeline.fit(x_train, y_train)
    # training complete

    metrics = {}

    # evaluate on training set
    y_train_pred = pipeline.predict(x_train)
    metrics["training"] = evaluate_set(y_train, y_train_pred, pipeline.classes_)

    # evaluate on validation set
    y_val_pred = pipeline.predict(x_val)
    metrics["validation"] = evaluate_set(y_val, y_val_pred, pipeline.classes_)

    # save the entire pipeline (model and vectorizer)
    save_model(pipeline, pipeline_path, ("gzip", 3))

    return pipeline, metrics


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
        default="data/dataset.csv",
        help="Path to training data file (augmented or not) in CSV format",
    )
    parser.add_argument(
        "--pipeline",
        type=str,
        default="models/dune.pipeline.joblib.gz",
        help="Path to which the model file will be saved",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.15,
        help="Proportion of the data for validation set (default: 0.15)",
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
        pipeline_path=args.pipeline,
        random_state=args.random_state,
        test_size=args.test_size,
        max_features=args.max_features,
    )

    print("[dune]: training complete")


if __name__ == "__main__":
    main()
