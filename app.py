"""
API server for end-user access
"""

import secrets
from flask import Flask, request, send_from_directory, jsonify


from src.predict import predict_command

app = Flask(__name__)

app.secret_key = secrets.token_hex()


@app.get("/")
def home():
    return send_from_directory("./app/dist/", "index.html")


@app.route("/<path:filepath>")
def render(filepath):
    return send_from_directory("./app/dist/", filepath)


@app.post("/api/predict")
def predict():
    try:
        text = request.json['text']
        result = predict_command(text)
        return jsonify({"status": "success", "message": "model responded", "action": result})
    except RuntimeError:
        return jsonify({"status": "error", "message": "something went wrong", "action": None})


if __name__ == "__main__":
    app.run("0.0.0.0", "5000", debug=True)
