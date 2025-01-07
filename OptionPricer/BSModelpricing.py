import numpy as np
from scipy.stats import norm
import requests
from bs4 import BeautifulSoup

# Option pricing function
def bs_price(spot, strike, rate, time, vol):
    d1 = (np.log(spot / strike) + (rate + 0.5 * vol**2) * time) / (vol * np.sqrt(time))
    d2 = d1 - vol * np.sqrt(time)
    return round(spot * norm.cdf(d1) - strike * np.exp(-rate * time) * norm.cdf(d2), 3)

# Generate prices for multiple strikes
def get_prices(stock, strikes, rate, time, vol):
    return {strike: bs_price(stock, strike, rate, time, vol) for strike in strikes}

# Fetch previous close price
def fetch_close(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    elem = soup.find("span", string="Previous Close")
    if elem:
        close_price = elem.find_next("span").text.strip()
        return float(close_price.replace(",", ""))
    return None

# Ask for inputs or set default
ticker = input("Enter the stock ticker (e.g., AAPL): ").strip()
prev_close = fetch_close(ticker)

if prev_close:
    # Get user input for Black-Scholes parameters
    try:
        interest_rate = float(input("Enter the risk-free interest rate (e.g., 0.0458): ").strip())
        time_to_expiry = float(input("Enter the time to expiry in years (e.g., 0.5): ").strip())
        volatility = float(input("Enter the volatility (e.g., 0.2): ").strip())
    except ValueError:
        print("Invalid input. Please provide numerical values.")
        exit()

    start_price = prev_close - 10
    step_size = 2.5 if start_price < 25 else 5 if start_price <= 200 else 10
    strike_list = [round(start_price + i * step_size, 2) for i in range(5)]

    # Calculate option prices
    prices = get_prices(prev_close, strike_list, interest_rate, time_to_expiry, volatility)

    print(f"Previous Close for {ticker}: {prev_close}")
    print("Strike Prices:", strike_list)
    print("Option Prices:", prices)
else:
    print(f"Could not fetch price for {ticker}")
