import tkinter as tk
from tkinter import ttk
import yfinance as yf
import datetime
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to fetch VIX data
vix_ticker = yf.Ticker("^VIX")
today = datetime.date.today().strftime("%Y-%m-%d")
vix_data = vix_ticker.history(start="2020-01-01", end=today)
vix_data = vix_data["Close"]

def vixvalue(date):
    if not isinstance(date, datetime.date):
        raise TypeError("The 'date' parameter must be of type datetime.date")
    date_str = date.strftime("%Y-%m-%d")
    vix_value = vix_data.loc[date_str]
    return vix_value

def VolTimeframe(date):
    annual_v = vixvalue(date)
    Vol_Daily = (annual_v / math.sqrt(252)) / 100
    Vol_Weekly = (annual_v / math.sqrt(52)) / 100
    Vol_Monthly = (annual_v / math.sqrt(12)) / 100
    All_Vols = [Vol_Daily, Vol_Weekly, Vol_Monthly]
    return All_Vols

def LoadTicker(ticker_symbol, interval):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="5y", interval=interval)
    return data["Close"]

def GetCloses(ticker_symbol, date):
    date_str = date.strftime("%Y-%m-%d")
    Daily_data = LoadTicker(ticker_symbol, "1d")
    Weekly_data = LoadTicker(ticker_symbol, "1wk")
    Monthly_data = LoadTicker(ticker_symbol, "1mo")
    if Daily_data is None or Weekly_data is None or Monthly_data is None:
        return None
    daily_close = Daily_data.loc[date_str]
    weekly_dates = Weekly_data.index
    weekly_date = weekly_dates[weekly_dates <= date_str].max()
    weekly_close = Weekly_data.loc[weekly_date]
    monthly_dates = Monthly_data.index
    monthly_date = monthly_dates[monthly_dates <= date_str].max()
    monthly_close = Monthly_data.loc[monthly_date]
    Closes = [float(daily_close), float(weekly_close), float(monthly_close)]
    return Closes

def CalculateLevels(ticker_symbol, date):
    Closes = GetCloses(ticker_symbol, date)
    AllVols = VolTimeframe(date)
    Daily_levels = [
        (AllVols[0] * Closes[0]) + Closes[0],  # SD+1
        (2 * AllVols[0] * Closes[0]) + Closes[0],  # SD+2
        (3 * AllVols[0] * Closes[0]) + Closes[0],  # SD+3
        (-AllVols[0] * Closes[0]) + Closes[0],  # SD-1
        (-2 * AllVols[0] * Closes[0]) + Closes[0],  # SD-2
        (-3 * AllVols[0] * Closes[0]) + Closes[0],  # SD-3
    ]
    weekly_levels = [
        AllVols[1] * Closes[1] + Closes[1],  # SD+1
        2 * AllVols[1] * Closes[1] + Closes[1],  # SD+2
        3 * AllVols[1] * Closes[1] + Closes[1],  # SD+3
        -AllVols[1] * Closes[1] + Closes[1],  # SD-1
        -2 * AllVols[1] * Closes[1] + Closes[1],  # SD-2
        -3 * AllVols[1] * Closes[1] + Closes[1],  # SD-3
    ]
    monthly_levels = [
        AllVols[2] * Closes[2] + Closes[2],  # SD+1
        2 * AllVols[2] * Closes[2] + Closes[2],  # SD+2
        3 * AllVols[2] * Closes[2] + Closes[2],  # SD+3
        -AllVols[2] * Closes[2] + Closes[2],  # SD-1
        -2 * AllVols[2] * Closes[2] + Closes[2],  # SD-2
        -3 * AllVols[2] * Closes[2] + Closes[2],  # SD-3
    ]
    Levels = [Daily_levels, weekly_levels, monthly_levels]
    return Levels

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Probability Levels")
        self.root.geometry("500x400")
        self.root.configure(bg="#f0f0f0")

        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.configure(relief="sunken", borderwidth=2)

        self.title_label = ttk.Label(self.main_frame, text="Probability Levels Calculator", font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Label(self.input_frame, text="Date (YYYY-MM-DD):", font=("Helvetica", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = ttk.Entry(self.input_frame, width=20, font=("Helvetica", 10))
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Ticker Symbol:", font=("Helvetica", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ticker_entry = ttk.Entry(self.input_frame, width=20, font=("Helvetica", 10))
        self.ticker_entry.grid(row=1, column=1, padx=5, pady=5)

        self.calculate_button = ttk.Button(self.main_frame, text="Calculate", command=self.calculate, style="Accent.TButton")
        self.calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.display_chart_button = ttk.Button(self.main_frame, text="Display Chart", command=self.display_chart, style="Accent.TButton")
        self.display_chart_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.result_frame = ttk.Frame(self.main_frame, padding="10")
        self.result_frame.grid(row=4, column=0, columnspan=2, pady=10)
        self.result_frame.configure(relief="sunken", borderwidth=2)

        self.result_label = ttk.Label(self.result_frame, text="Results will be displayed here", font=("Helvetica", 10), wraplength=400)
        self.result_label.grid(row=0, column=0)

        self.style = ttk.Style()
        self.style.configure("Accent.TButton", font=("Helvetica", 10, "bold"), background="#4CAF50", foreground="white")
        self.style.map("Accent.TButton", background=[("active", "#45a049")])

    def calculate(self):
        date_str = self.date_entry.get()
        ticker_symbol = self.ticker_entry.get()
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            levels = CalculateLevels(ticker_symbol, date)
            result_text = (
                f"Daily Levels (SD+1, SD+2, SD+3): {round(float(levels[0][0]), 2), round(float(levels[0][1]), 2), round(float(levels[0][2]), 2)}\n"
                f"Daily Levels (SD-1, SD-2, SD-3): {round(float(levels[0][3]), 2), round(float(levels[0][4]), 2), round(float(levels[0][5]), 2)}\n"
                f"Weekly Levels (SD+1, SD+2, SD+3): {round(float(levels[1][0]), 2), round(float(levels[1][1]), 2), round(float(levels[1][2]), 2)}\n"
                f"Weekly Levels (SD-1, SD-2, SD-3): {round(float(levels[1][3]), 2), round(float(levels[1][4]), 2), round(float(levels[1][5]), 2)}\n"
                f"Monthly Levels (SD+1, SD+2, SD+3): {round(float(levels[2][0]), 2), round(float(levels[2][1]), 2), round(float(levels[2][2]), 2)}\n"
                f"Monthly Levels (SD-1, SD-2, SD-3): {round(float(levels[2][3]), 2), round(float(levels[2][4]), 2), round(float(levels[2][5]), 2)}"
            )
            self.result_label.config(text=result_text, foreground="green")
        except Exception as e:
            self.result_label.config(text=f"This Date is a weekend or a holiday :) : {str(e)}", foreground="red")

    def display_chart(self):
        ticker_symbol = self.ticker_entry.get()
        date_str = self.date_entry.get()
        if not ticker_symbol or not date_str:
            self.result_label.config(text="Please enter a ticker symbol and date.", foreground="red")
            return

        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            levels = CalculateLevels(ticker_symbol, date)

            ticker = yf.Ticker(ticker_symbol)
            data = ticker.history(period="1y", interval="1d") 
            if data.empty:
                self.result_label.config(text="No data found for the ticker symbol.", foreground="red")
                return

            fig, ax = plt.subplots(figsize=(20, 10))
            ax.plot(data.index, data["Close"], label="Close Price", color="blue")

            # Daily Levels
            ax.axhline(y=levels[0][0], color="green", linestyle="--", label="Daily SD+1")
            ax.axhline(y=levels[0][1], color="orange", linestyle="--", label="Daily SD+2")
            ax.axhline(y=levels[0][2], color="red", linestyle="--", label="Daily SD+3")
            ax.axhline(y=levels[0][3], color="green", linestyle=":", label="Daily SD-1")
            ax.axhline(y=levels[0][4], color="orange", linestyle=":", label="Daily SD-2")
            ax.axhline(y=levels[0][5], color="red", linestyle=":", label="Daily SD-3")

            # Weekly Levels
            ax.axhline(y=levels[1][0], color="blue", linestyle="--", label="Weekly SD+1")
            ax.axhline(y=levels[1][1], color="purple", linestyle="--", label="Weekly SD+2")
            ax.axhline(y=levels[1][2], color="brown", linestyle="--")
            ax.axhline(y=levels[1][3], color="blue", linestyle=":", label="Weekly SD-1")
            ax.axhline(y=levels[1][4], color="purple", linestyle=":", label="Weekly SD-2")
            ax.axhline(y=levels[1][5], color="brown", linestyle=":")

            # Monthly Levels
            ax.axhline(y=levels[2][0], color="cyan", linestyle="--", label="Monthly SD+1")
            ax.axhline(y=levels[2][1], color="magenta", linestyle="--", label="Monthly SD+2")
            ax.axhline(y=levels[2][2], color="yellow", linestyle="--")
            ax.axhline(y=levels[2][3], color="cyan", linestyle=":", label="Monthly SD-1")
            ax.axhline(y=levels[2][4], color="magenta", linestyle=":", label="Monthly SD-2")
            ax.axhline(y=levels[2][5], color="yellow", linestyle=":")

            ax.set_title(f"{ticker_symbol} Closing Prices with SD Levels (1 Year)")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price (USD)")
            ax.legend()
            ax.grid(True)

            chart_window = tk.Toplevel(self.root)
            chart_window.title(f"{ticker_symbol} Price Chart with SD Levels")
            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack()

        except Exception as e:
            self.result_label.config(text=f"Error displaying chart: {str(e)}", foreground="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()