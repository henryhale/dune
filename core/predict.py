"""
Inference pipeline for command prediction
"""

import argparse
from utils import load_model
from preprocess import clean_text


class Predictor:
    """
    Wrapper class for command prediction - singleton with lazy-loaded instance
    """

    def __init__(
        self,
        vectorizer_path="models/dune.vectorizer.joblib",
        model_path="models/dune.model.joblib",
        confidence_threshold=0.6,
    ):
        """
        Initialize predictor

        Args:
            vectorizer_path (str): Path to vectorizer file
            model_path (str): Path to model file
            confidence_threshold (float): Minimum confidence for prediction
        """
        self.vectorizer = load_model(vectorizer_path)
        self.model = load_model(model_path)
        self.confidence_threshold = confidence_threshold

    def predict(self, text):
        """
        Predict command from user prompt

        Args:
            text (str): Input text

        Returns:
            dict: Prediction results with keys
                - command: predicted command
                - confidence: confidence score (0-1)
                - raw_text: original input text
        """
        # preprocess text
        text_cleaned = clean_text(text)

        # vectorize input
        x = self.vectorizer.transform([text_cleaned])

        # get probabilities
        probabilities = self.model._predict_proba_lr(x)[0]

        # get prediction
        predicted_index = probabilities.argmax()
        command = self.model.classes_[predicted_index]
        confidence = probabilities[predicted_index]

        # apply confidence threshold
        if confidence < self.confidence_threshold:
            command = "NOOP"

        return {
            "command": command,
            "confidence": confidence,
            "raw_text": text,
        }


# global shared predictor instance
_predictor = None


def predict_command(
    text,
    vectorizer_path="models/dune.vectorizer.joblib",
    model_path="models/dune.model.joblib",
    confidence_threshold=0.6,
):
    """
    Predict the output class given a user prompt

    Args:
        text (str): Input text
        vectorizer_path (str): Path to vectorizer file
        model_path (str): Path to model file
        confidence_threshold (float): Minimum confidence for prediction

    Returns:
        dict: Prediction results with keys
            - command: predicted command
            - confidence: confidence score (0-1)
            - raw_text: original input text
    """
    global _predictor

    if _predictor is None:
        _predictor = Predictor(vectorizer_path, model_path, confidence_threshold)

    return _predictor.predict(text)


def main():
    """
    A command line interface for making prediction
    """
    parser = argparse.ArgumentParser(
        description="Predict a command from user prompt or text"
    )
    parser.add_argument("text", type=str, nargs="?", help="Text to classify")
    parser.add_argument(
        "--vectorizer",
        type=str,
        default="models/dune.vectorizer.joblib",
        help="Path to vectorizer file",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="models/dune.model.joblib",
        help="Path to model file",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.6,
        help="Minimum confidence for prediction (default: 0.6)",
    )
    parser.add_argument(
        "--interactive", action='store_true', help="Run in interactive mode"
    )

    args = parser.parse_args()

    predictor = Predictor(args.vectorizer, args.model, args.threshold)

    if args.interactive:
        print("\nDune - a text-to-command predictor ")
        print("")
        print("Running in interactive mode")
        print("")
        print("Type 'quit' or 'exit' to stop\n")

        while True:
            try:
                text = input("> ")

                if text.lower() in ["quit", "exit"]:
                    print("\nGoodbye!")
                    break

                if not text:
                    continue

                result = predictor.predict(text)

                print(f"command: {result['command']}")
                print(f"confidence: {result['confidence']}")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
    elif args.text:
        result = predictor.predict(args.text)

        print(f"input: {result['raw_text']}")
        print(f"command: {result['command']}")
        print(f"confidence: {result['confidence']}")
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
