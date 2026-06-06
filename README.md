# 📈 Stock Price Prediction Model

A Machine Learning-based Stock Price Prediction application that forecasts future stock prices using historical market data and technical indicators. The project provides an interactive Streamlit dashboard where users can analyze stock trends and generate future price predictions using Linear Regression and Random Forest Regression models.

---

## 🚀 Features

- Fetches real-time historical stock market data using Yahoo Finance.
- Supports any valid stock ticker symbol.
- Calculates important technical indicators:
  - Simple Moving Average (SMA-20)
  - Exponential Moving Average (EMA-20)
  - Relative Strength Index (RSI)
- Implements two Machine Learning models:
  - Linear Regression
  - Random Forest Regression
- Predicts stock prices up to 60 business days ahead.
- Interactive Streamlit dashboard for visualization and prediction.
- Displays stock trends and technical indicators through charts.

---

## 🛠️ Technologies Used

### Programming Language
- Python

### Libraries & Frameworks
- Streamlit
- Pandas
- NumPy
- Scikit-Learn
- Yahoo Finance (yfinance)

### Machine Learning Models
- Linear Regression
- Random Forest Regressor

---

## 📂 Project Structure

```text
Stock-Price-Prediction/
│
├── model2.py
├── stock_price_prediction_linear_regression_Random_Forest.ipynb
├── README.md
└── requirements.txt
```

---

## 📊 Project Workflow

### 1. Data Collection

The application downloads historical stock market data from Yahoo Finance using the selected stock ticker and date range.

### 2. Data Preprocessing

The downloaded data is cleaned and transformed before training.

### 3. Feature Engineering

The following technical indicators are generated:

- SMA (20-day Moving Average)
- EMA (20-day Exponential Moving Average)
- RSI (Relative Strength Index)

These indicators serve as input features for the machine learning models.

### 4. Model Training

Users can choose between:

#### Linear Regression
A simple statistical model that captures overall market trends.

#### Random Forest Regression
An ensemble learning model capable of handling non-linear relationships in stock price movements.

### 5. Future Price Prediction

The selected model predicts future stock prices based on historical trends and generated technical indicators.

### 6. Visualization

The application displays:

- Historical Closing Prices
- SMA and EMA Trends
- RSI Indicator
- Future Predicted Prices

---

## ⚙️ Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/stock-price-prediction.git
cd stock-price-prediction
```

### Step 2: Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Packages

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install streamlit
pip install yfinance
pip install pandas
pip install numpy
pip install scikit-learn
```

---

## ▶️ Running the Application

Run the Streamlit application using:

```bash
streamlit run model2.py
```

After running the command, Streamlit will generate a local URL similar to:

```text
http://localhost:8501
```

Open the URL in your browser.

---

## 📝 How to Use

### Step 1
Enter a Stock Ticker Symbol.

Examples:

```text
AAPL
MSFT
TSLA
GOOG
RELIANCE.NS
TCS.NS
```

### Step 2
Select:

- Start Date
- End Date

### Step 3
Choose a Prediction Model:

```text
Linear Regression
Random Forest
```

### Step 4
Select the number of days ahead to predict.

Range:

```text
1 - 60 Days
```

### Step 5
Click **Apply**.

The application will:

- Download stock data
- Calculate technical indicators
- Train the selected model
- Display charts
- Generate future stock price predictions

---

## 📈 Example

### Input

```text
Ticker: AAPL
Start Date: 2020-01-01
End Date: 2024-12-31
Model: Random Forest
Prediction Days: 10
```

### Output

```text
2025-01-01 → $245.60
2025-01-02 → $246.11
2025-01-03 → $247.42
...
```

---

## 🔍 Key Technical Indicators

### Simple Moving Average (SMA)

Measures the average stock price over a specified period and helps identify trends.

### Exponential Moving Average (EMA)

Gives more weight to recent prices, making it more responsive to recent market changes.

### Relative Strength Index (RSI)

A momentum indicator used to identify overbought or oversold conditions.

---

## ⚠️ Limitations

- Predictions are based only on historical stock data.
- External factors such as news, earnings reports, economic events, and market sentiment are not considered.
- Long-term predictions may be less accurate due to market volatility.
- This project is intended for educational and research purposes only and should not be considered financial advice.

---

## 🚀 Future Enhancements

- Integration of XGBoost and LSTM models
- Sentiment Analysis using financial news
- Candlestick chart visualization
- Portfolio performance tracking
- Model accuracy comparison dashboard
- Real-time prediction updates

---

## 👨‍💻 Author

**Anmol Kumar**

B.Tech Information Technology  
KIIT University

Summer Intern – Tata Motors

### Skills Demonstrated

- Data Collection & Processing
- Feature Engineering
- Machine Learning
- Data Visualization
- Financial Data Analysis
- Streamlit Application Development

---

## 📜 License

This project is developed for educational and learning purposes.
