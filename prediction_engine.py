from __future__ import annotations

from datetime import timedelta

import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


FEATURES = ["Date_Ordinal", "SMA_20", "EMA_20", "RSI"]
MODEL_NAMES = {"linear": "Linear Regression", "random_forest": "Random Forest"}


def load_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    data = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=False)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    return data.dropna(how="all")


def compute_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window=window).mean()
    loss = (-delta.clip(upper=0)).rolling(window=window).mean()
    rs = gain / loss.replace(0, np.nan)
    return (100 - (100 / (1 + rs))).fillna(100)


def add_technical_indicators(data: pd.DataFrame) -> pd.DataFrame:
    enriched = data.copy()
    enriched["SMA_20"] = enriched["Close"].rolling(window=20).mean()
    enriched["EMA_20"] = enriched["Close"].ewm(span=20, adjust=False).mean()
    enriched["RSI"] = compute_rsi(enriched["Close"])
    return enriched


def prepare_model_frame(data: pd.DataFrame) -> pd.DataFrame:
    model_data = add_technical_indicators(data).reset_index()
    model_data["Date_Ordinal"] = pd.to_datetime(model_data["Date"]).map(pd.Timestamp.toordinal)
    return model_data.dropna(subset=FEATURES + ["Close"])


def build_model(model_key: str):
    if model_key == "linear":
        return LinearRegression()
    if model_key == "random_forest":
        return RandomForestRegressor(n_estimators=300, min_samples_leaf=2, random_state=42)
    raise ValueError("Unsupported model. Choose linear or random_forest.")


def evaluate_model(model_data: pd.DataFrame, model_key: str):
    if len(model_data) < 60:
        raise ValueError("Not enough historical rows after indicators are calculated. Try a wider date range.")

    x = model_data[FEATURES]
    y = model_data["Close"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=False)

    model = build_model(model_key)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    metrics = {
        "mae": round(float(mean_absolute_error(y_test, predictions)), 4),
        "r2": round(float(r2_score(y_test, predictions)), 4),
    }

    model.fit(x, y)
    return model, metrics


def forecast_prices(model, model_data: pd.DataFrame, days_ahead: int) -> list[dict]:
    close_history = model_data["Close"].tail(30).astype(float).tolist()
    base_date = pd.to_datetime(model_data["Date"].max())
    rows = []

    for index in range(1, days_ahead + 1):
        predict_date = pd.bdate_range(start=base_date + timedelta(days=1), periods=index)[-1]
        sma_20 = float(np.mean(close_history[-20:]))
        ema_20 = float(pd.Series(close_history).ewm(span=20, adjust=False).mean().iloc[-1])
        rsi = float(compute_rsi(pd.Series(close_history), window=14).iloc[-1])
        features = pd.DataFrame([[predict_date.toordinal(), sma_20, ema_20, rsi]], columns=FEATURES)

        prediction = round(float(model.predict(features)[0]), 2)
        close_history.append(prediction)
        rows.append({"date": predict_date.strftime("%Y-%m-%d"), "close": prediction})

    return rows


def series_payload(data: pd.DataFrame) -> list[dict]:
    chart_data = add_technical_indicators(data).reset_index()
    chart_data = chart_data.tail(220)
    rows = []

    for _, row in chart_data.iterrows():
        rows.append(
            {
                "date": pd.to_datetime(row["Date"]).strftime("%Y-%m-%d"),
                "close": _number(row["Close"]),
                "sma20": _number(row["SMA_20"]),
                "ema20": _number(row["EMA_20"]),
                "rsi": _number(row["RSI"]),
            }
        )

    return rows


def predict_stock(ticker: str, start: str, end: str, days_ahead: int, model_key: str) -> dict:
    ticker = ticker.strip().upper()
    days_ahead = int(days_ahead)

    if not ticker:
        raise ValueError("Ticker is required.")
    if days_ahead < 1 or days_ahead > 60:
        raise ValueError("Days ahead must be between 1 and 60.")
    if pd.to_datetime(start) >= pd.to_datetime(end):
        raise ValueError("Start date must be earlier than end date.")

    raw_data = load_data(ticker, start, end)
    if raw_data.empty:
        raise ValueError("No data found. Check the ticker symbol and date range.")

    model_data = prepare_model_frame(raw_data)
    model, metrics = evaluate_model(model_data, model_key)
    forecast = forecast_prices(model, model_data, days_ahead)
    latest_close = round(float(raw_data["Close"].iloc[-1]), 2)

    return {
        "ticker": ticker,
        "model": MODEL_NAMES.get(model_key, model_key),
        "currency": "Rs " if ticker.endswith((".NS", ".BO")) else "$",
        "latestClose": latest_close,
        "metrics": metrics,
        "history": series_payload(raw_data),
        "forecast": forecast,
    }


def _number(value):
    if pd.isna(value):
        return None
    return round(float(value), 4)
