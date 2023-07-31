"""
Purpose: Illustrate addition of continuous information. 

This is a simple example that uses a deque to store the last 15 minutes of
temperature readings for three locations.

The data is updated every minute.

Continuous information might also come from a database, a data lake, a data warehouse, or a cloud service.

----------------------------
Live Stock Price Information
-----------------------------

This app uses the live stock price data from Yahoo Finance API.

-----------------------
Keeping Secrets Secret
-----------------------

Keep secrets in a .env file - load it, read the values.
Add the .env file to your .gitignore so you don't publish it to GitHub.
We usually include a .env-example file to illustrate the format.

"""
#Standard imports
import asyncio
import os
from random import randint

#External Imports
import pandas as pd
import yfinance as yf
from collections import deque
from pathlib import Path

#Local Imports
from util_logger import setup_logger

logger, log_filename = setup_logger(__file__)

def lookup_ticker(company):
    stocks_dictionary = {
        "Wolverine World Wide Inc": "WWW",
        "Nice Inc": "NKE",
        "Lululemon Athletica Inc": "LULU",
        "Under Armour Inc": "UA",
        "On Holding AG": "ONON",
    }
    ticker = stocks_dictionary[company]
    return ticker

async def get_stock_price(ticker):
    logger.info("Calling get_stock_price for {ticker}}")
    # stock = yf.Ticker(ticker) # Get the stock data
    # price = stock.history(period="1d").tail(1)["Close"][0] # Get the closing price
    price = randint(132, 148) 
    return price

# Function to create or overwrite the CSV file with column headings
def init_csv_file(file_path):
    df_empty = pd.DataFrame(
        columns=["Company", "Ticker", "Time", "Price"]
    )
    df_empty.to_csv(file_path, index=False) 

async def update_csv_stock():
    