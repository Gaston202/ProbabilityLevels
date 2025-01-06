import tkinter as tk
from tkinter import ttk
import yfinance as yf
import pandas as pd
import datetime


vix_ticker = yf.Ticker("^VIX")
today = datetime.date.today().strftime("%Y-%m-%d")
vix_data = vix_ticker.history(start="2020-01-01", end=today)
vix_data=vix_data["Close"]
print(vix_data.head())
def vixvalue(date):
    if not isinstance(date, datetime.date):
        raise TypeError("The 'date' parameter must be of type datetime.date")
    
    date_str = date.strftime("%Y-%m-%d")
    vix_value = vix_data.loc[date_str]

    return vix_value

date1=datetime.date(2024,5,2)
value=vixvalue(date1)
print(f"Vix value on {date1} is {value}")