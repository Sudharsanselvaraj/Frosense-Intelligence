from flask import Flask, request, jsonify
from model_logic import get_decision

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message":"Sustainable AI Cold Storage Backend Active"})

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data:
        return jsonify({"error":"No JSON data received"}), 400
    result = get_decision(data)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
