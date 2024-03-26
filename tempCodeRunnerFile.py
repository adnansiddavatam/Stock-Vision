import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from forex_python.converter import CurrencyRates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys  # Import sys to use sys.exit()

def fetch_and_plot():
    # Clearing previous figure in the GUI
    for widget in frame.winfo_children():
        widget.destroy()

    # Retrieving values from the GUI
    ticker_symbol = symbol_entry.get().upper()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    currency = currency_entry.get().upper()

    # Fetch historical stock data
    data = yf.download(ticker_symbol, start=start_date, end=end_date)

    # Convert the Close price to the desired currency
    c = CurrencyRates()
    current_rate = c.get_rate('USD', currency)
    data['Close'] = data['Close'] * current_rate
    data['SMA_20'] = data['Close'].rolling(window=20).mean()

    # Plotting
    fig, ax = plt.subplots()
    ax.plot(data['Close'], label=f'{ticker_symbol} Close Price', alpha=0.5)
    ax.plot(data['SMA_20'], label='20-Day SMA', color='orange', alpha=0.75)
    ax.set_title(f'{ticker_symbol} Close Price and 20-Day SMA in {currency}')
    ax.set_xlabel('Date')
    ax.set_ylabel(f'Price ({currency})')
    ax.legend()

    # Integrating matplotlib figure into Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=frame)  
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()
    canvas.draw()

def on_closing():
    window.destroy()
    sys.exit()

# Setting up the GUI window
window = tk.Tk()
window.title("Stock Vision")

# Creating the input fields
tk.Label(window, text="Stock Ticker Symbol:").grid(row=0)
symbol_entry = tk.Entry(window)
symbol_entry.grid(row=0, column=1)

tk.Label(window, text="Start Date (YYYY-MM-DD):").grid(row=1)
start_date_entry = tk.Entry(window)
start_date_entry.grid(row=1, column=1)

tk.Label(window, text="End Date (YYYY-MM-DD):").grid(row=2)
end_date_entry = tk.Entry(window)
end_date_entry.grid(row=2, column=1)

tk.Label(window, text="Currency (e.g., USD):").grid(row=3)
currency_entry = tk.Entry(window)
currency_entry.grid(row=3, column=1)

# Submit button
submit_button = ttk.Button(window, text="Analyze", command=fetch_and_plot)
submit_button.grid(row=4, column=0, columnspan=2)

# Frame for matplotlib canvas
frame = tk.Frame(window)
frame.grid(row=5, column=0, columnspan=4)

window.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window closing

window.mainloop()
