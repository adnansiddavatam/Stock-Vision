import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from forex_python.converter import CurrencyRates

# User inputs for ticker symbol, start date, and end date
ticker_symbol = input("Enter the stock ticker symbol (e.g., AAPL): ")
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")
currency = input("Enter the currency you want to convert to (e.g., CAD): ").upper()

# Fetch historical stock data
data = yf.download(ticker_symbol, start=start_date, end=end_date)

# Convert the Close price to the desired currency
c = CurrencyRates()
# Get the current conversion rate; this example assumes the stock prices are in USD
current_rate = c.get_rate('USD', currency)

# Apply the current conversion rate to the Close prices
data['Close'] = data['Close'] * current_rate
data['SMA_20'] = data['Close'].rolling(window=20).mean()

# Plotting
plt.figure(figsize=(14, 7))
plt.plot(data['Close'], label=f'{ticker_symbol} Close Price', alpha=0.5)
plt.plot(data['SMA_20'], label='20-Day SMA', color='orange', alpha=0.75)
plt.title(f'{ticker_symbol} Close Price and 20-Day SMA in {currency}')
plt.xlabel('Date')
plt.ylabel(f'Price ({currency})')
plt.legend()
plt.show()
