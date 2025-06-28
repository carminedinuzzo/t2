"""Simple Flask web server to interact with the local AI node."""

import logging
from pathlib import Path

from flask import Flask, render_template, request, jsonify
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Address of the local node exposed via tunnel
LOCAL_NODE_URL = "http://localhost:8000"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    message = request.form.get("message")
    if not message:
        return jsonify({"error": "no message"}), 400
    logger.debug("Forwarding message to local node: %s", message)
    resp = requests.post(f"{LOCAL_NODE_URL}/ask", json={"message": message})
    if resp.status_code != 200:
        return jsonify({"error": resp.text}), resp.status_code
    return jsonify(resp.json())


@app.route("/history")
def history():
    resp = requests.get(f"{LOCAL_NODE_URL}/history")
    return jsonify(resp.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
