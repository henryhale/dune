import joblib


def export_model(model, vectorizer, model_path=None, vectorizer_path=None):
    """
    Save the model and vectorizer in separate files.
    """
    model_file_path = model_path if model_path is not None else "model.joblib"
    joblib.dump(model, filename=model_file_path)

    vectorizer_file_path = (
        vectorizer_path if model_path is not None else "vectorizer.joblib"
    )
    joblib.dump(vectorizer, filename=vectorizer_file_path)


def load_model(model_file_path, vectorizer_file_path):
    """
    Load the model in to memory
    """
    vectorizer = joblib.load(vectorizer_file_path)
    model = joblib.load(model_file_path)
    return model, vectorizer
