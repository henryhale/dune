from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import pandas


def split_data(df: pandas.DataFrame, val_test_size=0.3):
    """
    Splits the data into training and temp sets.
    The temp set is then split by half to create validation and testing sets.
    """
    x = df["cleaned_text"]
    y = df["encoded_label"]

    # first split: train, temp (for validation/test)
    x_train, x_temp, y_train, y_temp = train_test_split(
        x, y, test_size=val_test_size, random_state=42, stratify=y
    )

    # second split: validation & test as 50/50 of temp
    x_val, x_test, y_val, y_test = train_test_split(
        x_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )

    return x_train, x_val, x_test, y_train, y_val, y_test


def train_model(x, y, max_features=5000):
    """
    Trains the model on the features(x) and classes(y)

    Returns a vectorizer and LinearSVM model
    """
    # use `max_features` to limit features for efficiency
    tfidf_vectorizer = TfidfVectorizer(max_features=max_features, lowercase=False)

    # fit on training data and transform training split
    x_train_tfidf = tfidf_vectorizer.fit_transform(x)

    # initialize svc model
    linear_svc_model = LinearSVC(
        random_state=42, dual=False
    )  # dual=False for n_samples > n_features

    # train model
    linear_svc_model.fit(x_train_tfidf, y)

    return tfidf_vectorizer, linear_svc_model
