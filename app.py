# app.py
from flask import Flask, request, jsonify
from model_logic import aggregate_storage

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Expects JSON POST from ESP or simulator:
    {
        "items": [
            {"label":"banana","temperature":14,"humidity":82,"ethylene":0.5,"ammonia":0.03,"h2s":0.04,"co2":0.18},
            {"label":"tomato","temperature":11,"humidity":78,"ethylene":0.3,"ammonia":0.02,"h2s":0.03,"co2":0.15}
        ]
    }
    """
    data = request.get_json()

    if not data or "items" not in data:
        return jsonify({"error":"No items provided"}), 400

    items_list = data["items"]

    dashboard = aggregate_storage(items_list)

    return jsonify(dashboard), 200


@app.route("/", methods=["GET"])
def home():
    return "<h2>Sustainable AI Cold Storage API is running.</h2>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
