"""
Inference pipeline for command prediction
"""

import argparse
from scipy.special import softmax
from src.utils import load_model
from src.preprocess import clean_text


class Predictor:
    """
    Wrapper class for command prediction - singleton with lazy-loaded instance
    """

    def __init__(
        self,
        pipeline_path="models/pipeline.joblib",
        confidence_threshold=0.1,
        quiet=True,
    ):
        """
        Initialize predictor

        Args:
            pipeline_path (str): Path to pipeline file
            confidence_threshold (float): Minimum confidence for prediction
            quiet (bool): Whether or not to display logs
        """
        self.pipeline = load_model(pipeline_path)
        self.confidence_threshold = confidence_threshold
        self.log = not bool(quiet)

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

        # get vectorizer from pipeline
        vectorizer = self.pipeline.named_steps["vectorizer"]
        # vectorize input
        x = vectorizer.transform([text_cleaned])

        # get model from pipeline
        model = self.pipeline.named_steps["classifier"]
        # get decision scores
        scores = model.decision_function(x)[0]
        if self.log:
            print("scores:", scores)

        probabilities = softmax(scores)
        if self.log:
            print("probabilities", probabilities)

        # get prediction
        predicted_index = probabilities.argmax()
        if self.log:
            print("predicted index:", predicted_index)

        command = model.classes_[predicted_index]
        if self.log:
            print("command:", command)

        confidence = probabilities[predicted_index]
        if self.log:
            print("confidence:", confidence)

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
    text, pipeline_path="models/pipeline.joblib", confidence_threshold=0.1, quiet=True
):
    """
    Predict the output class given a user prompt

    Args:
        text (str): Input text
        pipeline_path (str): Path to pipeline file
        confidence_threshold (float): Minimum confidence for prediction
        quiet (bool): Whether or not to display logs

    Returns:
        dict: Prediction results with keys
            - command: predicted command
            - confidence: confidence score (0-1)
            - raw_text: original input text
    """
    global _predictor

    if _predictor is None:
        _predictor = Predictor(pipeline_path, confidence_threshold, quiet)

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
        "--pipeline",
        type=str,
        default="models/pipeline.joblib",
        help="Path to pipeline file",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.1,
        help="Minimum confidence for prediction (default: 0.1)",
    )
    parser.add_argument(
        "--interactive", action="store_true", help="Run in interactive mode"
    )

    args = parser.parse_args()

    predictor = Predictor(args.pipeline, args.threshold, True)

    if args.interactive:
        print("\nDune - a text-to-command predictor")
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
                print(f"confidence: {result['confidence']}\n")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
    elif args.text:
        result = predictor.predict(args.text)

        print(f"\ninput: {result['raw_text']}")
        print(f"command: {result['command']}")
        print(f"confidence: {result['confidence']}\n")
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
