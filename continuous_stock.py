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
import datetime

#External Imports
import pandas as pd
from collections import deque
from pathlib import Path

#Local Imports
from util_logger import setup_logger
from fetch import fetch_from_url

logger, log_filename = setup_logger(__file__)

def lookup_ticker(company):
    stocks_dictionary = {
        "Wolverine World Wide Inc": "WWW",
        "Nike Inc": "NKE",
        "Lululemon Athletica Inc": "LULU",
        "Under Armour Inc": "UA",
        "On Holding AG": "ONON",
    }
    ticker = stocks_dictionary[company]
    return ticker

async def get_stock_price(ticker):
    logger.info("Calling get_stock_price for {ticker}}")
    url = f"https://query1.finance.yahoo.com/v7/finance/options/{ticker}"
    url_response = await fetch_from_url(url, "json")
    price = url_response.data["optionChain"]["result"][0]["quote"]["regularMarketPrice"]
    # price = randint(132, 148) 
    return price

# Function to create or overwrite the CSV file with column headings
def init_csv_file(file_path):
    df_empty = pd.DataFrame(
        columns=["Company", "Ticker", "Time", "Price"]
    )
    df_empty.to_csv(file_path, index=False) 

async def update_csv_stock():
    """Update the CSV file with the latest stock information."""
    logger.info("Calling update_csv_stock")
    try:
        companies = ["Wolverine World Wide Inc", "Nike Inc", "Lululemon Athletica Inc", "Under Armour Inc", "On Holding AG"]
        update_interval = 60  # Update every 1 minute (60 seconds)
        total_runtime = 15 * 60  # Total runtime maximum of 15 minutes
        num_updates = 10 * len(companies)  # Keep the most recent 10 readings
        logger.info(f"update_interval: {update_interval}")
        logger.info(f"total_runtime: {total_runtime}")
        logger.info(f"num_updates: {num_updates}")

        # Use a deque to store just the last, most recent 10 readings in order
        records_deque = deque(maxlen=num_updates)

        fp = Path(__file__).parent.joinpath("data").joinpath("mtcars_stock.csv")

        # Check if the file exists, if not, create it with only the column headings
        if not os.path.exists(fp):
            init_csv_file(fp)

        logger.info(f"Initialized csv file at {fp}")

        for _ in range(num_updates):  # To get num_updates readings
            for company in companies:
                ticker = lookup_ticker(company)
                new_price = await get_stock_price(ticker)
                time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current time
                new_record = {
                    "Company": company,
                    "Ticker": ticker,
                    "Time": time_now,
                    "Price": new_price,
                }
                records_deque.append(new_record)

            # Use the deque to make a DataFrame
            df = pd.DataFrame(records_deque)

            # Save the DataFrame to the CSV file, deleting its contents before writing
            df.to_csv(fp, index=False, mode="w")
            logger.info(f"Saving stocks to {fp}")

            # Wait for update_interval seconds before the next reading
            await asyncio.sleep(update_interval)

    except Exception as e:
        logger.error(f"ERROR in update_csv_stock: {e}")