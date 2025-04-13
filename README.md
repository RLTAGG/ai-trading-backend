# AI Trading Backend (Yahoo Finance Version)

This version pulls real-time stock prices from Yahoo Finance.

## 🔌 Usage

### POST to `/api/price`
```json
{ "ticker": "AAPL" }
```

Returns:
```json
{
  "price": 191.45,
  "signal": "BUY"
}
```

## Endpoints
- `/api/price` → fetch price for a stock and update strategy
- `/api/predict` → returns current signal
- `/api/execute` → logs real trades
- `/api/status` → view chart and trade logs

## 🧪 Run Locally
```bash
pip install -r requirements.txt
python server.py
```
