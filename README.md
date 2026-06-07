# Stock Prediction Studio

This project contains a custom browser frontend and a small Python API for forecasting stock closing prices with either Linear Regression or Random Forest models. It downloads historical data from Yahoo Finance, builds simple technical indicators, reports validation metrics, and shows a forward forecast for the selected number of business days.

## Files

- `server.py` - local HTTP server that serves the frontend and prediction API.
- `prediction_engine.py` - stock data, indicator, model, metric, and forecast logic.
- `frontend/` - HTML, CSS, and JavaScript app UI.
- `stock_price_prediction_linear_regression_Random_Forest.ipynb` - original exploratory notebook.
- `requirements.txt` - Python dependencies required by the API.

## Setup

```powershell
python -m pip install -r requirements.txt
```

## Run

```powershell
python server.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000), choose a ticker and date range, then click **Run prediction**.

## Notes

The forecasts are educational and should not be treated as financial advice. Stock prices are noisy, and simple models based on historical closing prices cannot reliably predict future market moves.
