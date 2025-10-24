# app.py
from flask import Flask, request, jsonify
from model_logic import aggregate_storage

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Accepts JSON POST from ESP8266:

    1️⃣ Single sensor JSON:
    {
        "label":"banana",
        "temperature":14,
        "humidity":82,
        "ethylene":0.5,
        "ammonia":0.03,
        "h2s":0.04,
        "co2":0.18
    }

    2️⃣ List of items:
    {
        "items":[
            {"label":"banana","temperature":14,"humidity":82,"ethylene":0.5,"ammonia":0.03,"h2s":0.04,"co2":0.18},
            {"label":"tomato","temperature":11,"humidity":78,"ethylene":0.3,"ammonia":0.02,"h2s":0.03,"co2":0.15}
        ]
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    # If 'items' key exists, use it; otherwise wrap single item
    if "items" in data:
        items_list = data["items"]
    else:
        items_list = [data]

    dashboard = aggregate_storage(items_list)

    return jsonify(dashboard), 200


@app.route("/", methods=["GET"])
def home():
    return "<h2>Sustainable AI Cold Storage API is running.</h2>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
