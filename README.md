# ProbabilityLevels

ProbabilityLevels is a Python desktop application that calculates and visualizes probability-based price levels (standard deviation bands) for financial instruments using historical price data and volatility (VIX). The app provides daily, weekly, and monthly standard deviation levels for any given ticker and date, and displays them on a chart alongside historical prices.

## Features

- **Calculate Probability Levels:**
  - Computes SD+1, SD+2, SD+3, SD-1, SD-2, SD-3 levels for daily, weekly, and monthly timeframes.
  - Uses VIX data to estimate volatility for each timeframe.
- **Interactive GUI:**
  - User-friendly interface built with Tkinter.
  - Input any stock ticker and date to get probability levels.
- **Chart Visualization:**
  - Plots the closing price with calculated SD levels for the past year using Matplotlib.
  - Visualizes daily, weekly, and monthly bands with distinct colors and styles.

## Requirements

- Python 3.7+
- [yfinance](https://pypi.org/project/yfinance/)
- [matplotlib](https://pypi.org/project/matplotlib/)
- [tkinter](https://docs.python.org/3/library/tkinter.html) (usually included with Python)

Install dependencies with:

```bash
pip install yfinance matplotlib
```

## Usage

1. Run the application:
   
   ```bash
   python ProjectProbability.py
   ```

2. Enter a date (YYYY-MM-DD) and a ticker symbol (e.g., AAPL, MSFT).
3. Click **Calculate** to see the probability levels.
4. Click **Display Chart** to view the price chart with SD levels.

## How It Works

- The app fetches VIX data to estimate annualized volatility.
- It retrieves historical close prices for the selected ticker on daily, weekly, and monthly intervals.
- Standard deviation levels are calculated for each timeframe and displayed.
- The chart overlays these levels on the price history for visual analysis.

## Notes

- The app requires an internet connection to fetch financial data.
- If the selected date is a weekend or holiday, an error message will be shown.
- VIX data is used as a proxy for market volatility; results are for educational purposes only.

## License

This project is provided for educational and personal use. No warranty is provided.

