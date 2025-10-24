# app.py
from flask import Flask, jsonify
from model_logic import aggregate_storage

app = Flask(__name__)

@app.route("/analyze", methods=["GET"])
def analyze():
    """
    No POST required. This API generates fully simulated
    cold storage readings, AI predictions, and alerts.
    """
    dashboard = aggregate_storage()
    return jsonify(dashboard), 200

@app.route("/", methods=["GET"])
def home():
    return "<h2>Sustainable AI Cold Storage Simulator API is running.</h2>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
