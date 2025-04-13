from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Trade state
price_history = []
trades_today = 0
auto_trade_enabled = True
last_signal = "HOLD"
executed_trades = []

MA_PERIOD = 3  # Simple moving average period

@app.route("/api/price", methods=["POST"])
def receive_price():
    global price_history, last_signal
    data = request.get_json()
    price = data.get("price")

    if price is None:
        return jsonify({"error": "Missing price"}), 400

    price_history.append(price)
    if len(price_history) > MA_PERIOD + 1:
        price_history = price_history[-(MA_PERIOD + 1):]

    if len(price_history) > MA_PERIOD:
        ma = sum(price_history[:-1]) / MA_PERIOD
        last_price = price_history[-1]
        if last_price > ma:
            last_signal = "BUY"
        elif last_price < ma:
            last_signal = "SELL"
        else:
            last_signal = "HOLD"

    return jsonify({"status": "price received", "signal": last_signal})


@app.route("/api/predict", methods=["GET"])
def predict():
    return jsonify({
        "signal": last_signal,
        "auto_trade": auto_trade_enabled
    })

@app.route("/api/execute", methods=["POST"])
def execute():
    global trades_today
    data = request.get_json()
    executed_trades.append({
        "signal": data.get("signal"),
        "timestamp": datetime.utcnow().isoformat()
    })
    trades_today += 1
    print(f"Executed trade: {data}")
    return jsonify({"status": "executed"})

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "last_signal": last_signal,
        "timestamp": datetime.utcnow().isoformat(),
        "trades_today": trades_today,
        "auto_trade_enabled": auto_trade_enabled,
        "executed_trades": executed_trades,
        "chart": {
            "timestamps": list(range(len(price_history))),
            "prices": price_history
        }
    })

@app.route("/api/set_auto_trade", methods=["POST"])
def set_auto_trade():
    global auto_trade_enabled
    data = request.get_json()
    auto_trade_enabled = data.get("enabled", True)
    return jsonify({"auto_trade_enabled": auto_trade_enabled})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
