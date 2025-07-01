"""Simple Flask web server to interact with the local AI node."""

import logging
import os
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session,
)
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-me")

# Login credentials from environment
USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
PASSWORD = os.environ.get("ADMIN_PASSWORD", "secret")

# Address of the local node exposed via tunnel
LOCAL_NODE_URL = "http://localhost:8000"


def login_required(func):
    """Decorator to require authentication."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return wrapper


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and password == PASSWORD:
            session["user"] = username
            return redirect(url_for("index"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/ask", methods=["POST"])
@login_required
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
@login_required
def history():
    resp = requests.get(f"{LOCAL_NODE_URL}/history")
    return jsonify(resp.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
