from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

mock_signal = "BUY"
auto_trade_enabled = True

mock_chart = {
    "timestamps": ["13:00", "13:15", "13:30", "13:45", "14:00"],
    "prices": [100, 102, 101, 105, 107]
}

@app.route("/api/predict", methods=["GET"])
def predict():
    return jsonify({
        "signal": mock_signal,
        "auto_trade": auto_trade_enabled
    })

@app.route("/api/execute", methods=["POST"])
def execute():
    data = request.get_json()
    print(f"Executed trade: {data}")
    return jsonify({"status": "success"})

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "last_signal": mock_signal,
        "timestamp": datetime.utcnow().isoformat(),
        "trades_today": 5,
        "auto_trade_enabled": auto_trade_enabled,
        "chart": mock_chart
    })

@app.route("/api/set_auto_trade", methods=["POST"])
def set_auto_trade():
    global auto_trade_enabled
    data = request.get_json()
    auto_trade_enabled = data.get("enabled", True)
    return jsonify({"auto_trade_enabled": auto_trade_enabled})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
