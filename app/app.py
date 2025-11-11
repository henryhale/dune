from flask import Flask, request, session
import uuid
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex()

@app.post("/")
def handle_request():
    if 'token' not in session:
        session['token'] = uuid.uuid4()
    session_token = session['token']
    
    