"""
API server for end-user access
"""

import argparse
import secrets
from flask import Flask, request, send_from_directory, jsonify


from src.predict import predict_command

app = Flask(__name__)

app.secret_key = secrets.token_hex()


@app.get("/")
def home():
    """
    Home page of the application 
    """
    return send_from_directory("./app/dist/", "index.html")


@app.route("/<path:filepath>")
def render(filepath):
    """
    Frontend assets of the application
    """
    return send_from_directory("./app/dist/", filepath)


@app.post("/api/predict")
def predict():
    """
    API endpoint for making predictions
    """
    try:
        text = request.json['text']
        result = predict_command(text)
        return jsonify({"status": "success", "message": "model responded", "action": result})
    except RuntimeError:
        return jsonify({"status": "error", "message": "something went wrong", "action": None})

def main():
    """
    A command line interface for running the full application server (frontend and API)
    """
    parser = argparse.ArgumentParser(
        description="CLI for running the application server"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Specify the hostname"
    )
    parser.add_argument(
        "--port", type=int, default="5000", help="Specify the port number"
    )
    parser.add_argument(
        "--debug", type=bool, default=False, help="Run server in debug mode"
    )

    args = parser.parse_args()

    app.run(args.host, args.port, debug=args.debug)


if __name__ == "__main__":
    main()
