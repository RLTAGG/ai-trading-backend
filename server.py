
from flask import Flask, request, jsonify
from flask_cors import CORS
import feedparser
import re

app = Flask(__name__)
CORS(app)

def fetch_yahoo_news_sentiment(ticker):
    rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    feed = feedparser.parse(rss_url)
    sentiment_score = 0
    headlines = []

    for entry in feed.entries[:5]:
        title = entry.title
        headlines.append(title)

        title_lower = title.lower()
        if any(w in title_lower for w in ["beats", "soars", "rises", "strong", "record", "growth"]):
            sentiment_score += 1
        elif any(w in title_lower for w in ["falls", "drops", "misses", "lawsuit", "crash", "weak"]):
            sentiment_score -= 1

    sentiment = "Bullish" if sentiment_score > 0 else "Bearish" if sentiment_score < 0 else "Neutral"
    return sentiment, headlines

@app.route("/api/news", methods=["POST"])
def get_news_sentiment():
    data = request.json
    ticker = data.get("ticker", "AAPL")
    sentiment, headlines = fetch_yahoo_news_sentiment(ticker)
    return jsonify({
        "sentiment": sentiment,
        "headlines": headlines
    })

@app.route("/api/whale", methods=["GET"])
def get_mock_whale_alert():
    return jsonify({
        "status": "buy",
        "type": "outflow",
        "amount_usd": 750000,
        "asset": "BTC",
        "exchange": "Binance"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
