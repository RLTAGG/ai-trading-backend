# AI Trading Backend (Real Executed Trades)

Tracks real executed trades only. Uses a simple moving average crossover strategy.

## Endpoints:

- POST /api/price → feed current price
- GET /api/predict → get current signal
- POST /api/execute → record a trade
- GET /api/status → see trade history and signal chart

## Run locally:
```bash
pip install -r requirements.txt
python server.py
```
