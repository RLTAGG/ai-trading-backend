
from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import datetime

app = Flask(__name__)
CORS(app)

TRADES = []
AUTO_TRADE = True

@app.route("/api/predict", methods=["GET"])
def predict():
    last_signal = "HOLD"
    if TRADES:
        last_signal = TRADES[-1]["signal"]
    return jsonify({
        "signal": last_signal,
        "auto_trade": AUTO_TRADE
    })

@app.route("/api/set_auto_trade", methods=["POST"])
def set_auto_trade():
    global AUTO_TRADE
    data = request.get_json()
    AUTO_TRADE = bool(data.get("enabled", True))
    return jsonify({"status": "ok", "auto_trade": AUTO_TRADE})

@app.route("/api/price", methods=["POST"])
def price():
    data = request.get_json()
    ticker = data.get("ticker", "AAPL")

    mock_price = round(random.uniform(150, 300), 2) if "AAPL" in ticker else round(random.uniform(8000, 90000), 2)
    ma = mock_price - random.uniform(-20, 20)
    adjusted = mock_price + random.uniform(-1, 1)
    signal = "BUY" if adjusted > ma else "SELL" if adjusted < ma else "HOLD"

    return jsonify({
        "debug": {
            "base_price": mock_price,
            "adjusted_price": adjusted,
            "MA": round(ma, 2)
        },
        "signal": signal
    })

@app.route("/api/execute", methods=["POST"])
def execute():
    data = request.get_json()
    signal = data.get("signal", "HOLD")
    timestamp = datetime.datetime.now().isoformat()
    TRADES.append({"signal": signal, "timestamp": timestamp})
    return jsonify({"status": "executed", "signal": signal})

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "trades_today": len(TRADES),
        "last_signal": TRADES[-1]["signal"] if TRADES else "HOLD"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
