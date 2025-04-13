# AI Trading Backend (Real Trading Setup)

This version supports logic-based trade signals using simple moving averages.

## 🧠 Features:
- Track live prices via `/api/price`
- Predict signal using MA strategy via `/api/predict`
- View trade stats and price chart via `/api/status`

## 🔄 Example:
POST price:
```
curl -X POST http://localhost:5000/api/price -H "Content-Type: application/json" -d '{"price": 105.2}'
```

Get signal:
```
curl http://localhost:5000/api/predict
```

## 🧪 Run locally:
```bash
pip install -r requirements.txt
python server.py
```
