from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import random
import yfinance as yf
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

price_history = {}
executed_trades = []
last_signals = {}
auto_trade_enabled = True
MA_PERIOD = 3

def fetch_price(ticker, source="yahoo"):
    try:
        if source == "yahoo":
            data = yf.Ticker(ticker).history(period="1d", interval="1m")
            if data.empty:
                raise Exception("Empty data from Yahoo")
            return float(data["Close"].iloc[-1])

        elif source == "binance":
            if ticker.lower() == "btc":
                symbol = "BTCUSDT"
            elif ticker.lower() == "eth":
                symbol = "ETHUSDT"
            else:
                raise Exception("Unsupported Binance symbol")

            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            res = requests.get(url)
            return float(res.json()["price"])

        elif source == "mock":
            return round(100 + random.uniform(-1, 1), 2)

        else:
            raise Exception("Unsupported feed")

    except Exception as e:
        print(f"Fetch error for {ticker} from {source}: {e}")
        return None

@app.route("/api/price", methods=["POST"])
def receive_price():
    global last_signals
    data = request.get_json()
    ticker = data.get("ticker")
    feed = data.get("feed", "yahoo")

    if not ticker:
        return jsonify({"error": "Missing ticker"}), 400

    price = fetch_price(ticker, feed)
    if price is None:
        return jsonify({"error": "Failed to fetch price"}), 500

    adjusted = round(price + random.uniform(-0.2, 0.2), 2)

    if ticker not in price_history:
        price_history[ticker] = []
    price_history[ticker].append(adjusted)
    if len(price_history[ticker]) > MA_PERIOD + 1:
        price_history[ticker] = price_history[ticker][-MA_PERIOD - 1:]

    debug = {
        "ticker": ticker,
        "feed": feed,
        "base": price,
        "adjusted": adjusted,
        "price_history": price_history[ticker].copy()
    }

    if len(price_history[ticker]) > MA_PERIOD:
        ma = sum(price_history[ticker][:-1]) / MA_PERIOD
        last = price_history[ticker][-1]
        debug["MA"] = round(ma, 2)
        debug["last_price"] = last

        if last > ma:
            signal = "BUY"
        elif last < ma:
            signal = "SELL"
        else:
            signal = "HOLD"
        last_signals[ticker] = signal
    else:
        signal = "HOLD"
        last_signals[ticker] = signal

    debug["signal"] = signal

    return jsonify({
        "status": "OK",
        "ticker": ticker,
        "feed": feed,
        "signal": signal,
        "debug": debug
    })

@app.route("/api/predict", methods=["GET"])
def predict():
    ticker = request.args.get("ticker", "AAPL")
    return jsonify({
        "signal": last_signals.get(ticker, "HOLD"),
        "auto_trade": auto_trade_enabled
    })

@app.route("/api/execute", methods=["POST"])
def execute():
    data = request.get_json()
    executed_trades.append({
        "signal": data.get("signal"),
        "ticker": data.get("ticker"),
        "timestamp": datetime.utcnow().isoformat()
    })
    return jsonify({"status": "executed"})

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "trades_today": len(executed_trades),
        "executed_trades": executed_trades,
        "auto_trade_enabled": auto_trade_enabled,
        "tickers": list(price_history.keys()),
        "chart_data": price_history
    })

@app.route("/api/set_auto_trade", methods=["POST"])
def toggle_auto_trade():
    global auto_trade_enabled
    data = request.get_json()
    auto_trade_enabled = data.get("enabled", True)
    return jsonify({"auto_trade_enabled": auto_trade_enabled})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
