import tkinter as tk
from tkinter import ttk
import yfinance as yf
import pandas as pd
import datetime
import math

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
def VolTimeframe (date):
    annual_v=vixvalue(date)
    Vol_Daily=annual_v/math.sqrt(252)
    Vol_Weekly=annual_v/math.sqrt(52)
    Vol_Monthly=annual_v/math.sqrt(12)
    All_Vols=[Vol_Daily,Vol_Weekly,Vol_Monthly]
    return All_Vols
def LoadTicker(ticker_symbol,interval):
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
def CalculateLevels(ticker_symbol,date):   

    Closes=GetCloses(ticker_symbol,date)
    AllVols=VolTimeframe(date)
    Daily_levels =[ AllVols[0] * Closes[0] +Closes[0] , 2*AllVols[0]*Closes[0]+Closes[0] , 3*AllVols[0]*Closes[0]+Closes[0] ]
    weekly_levels=[ AllVols[1] * Closes[1] +Closes[1] , 2*AllVols[1]*Closes[1]+Closes[1] , 3*AllVols[1]*Closes[1]+Closes[1] ]
    monthly_levels=[ AllVols[2] * Closes[2] +Closes[2] , 2*AllVols[2]*Closes[2]+Closes[2] , 3*AllVols[2]*Closes[2]+Closes[2] ]
    Levels=[Daily_levels,weekly_levels,monthly_levels]
    return Levels

ticker_symbol = "AAPL"
date = datetime.date(2023, 12, 6) 
closes = GetCloses(ticker_symbol, date)
print(closes)