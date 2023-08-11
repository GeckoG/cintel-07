# Standard Library
import asyncio
from datetime import datetime
from pathlib import Path
import os
from random import randint

# External Packages
import pandas as pd
from collections import deque
from dotenv import load_dotenv

# Local Imports
from util_logger import setup_logger

# Set up a file logger
logger, log_filename = setup_logger(__file__)


# async def get_temperature_from_openweathermap(lat, long):
#     logger.info("Calling get_temperature_from_openweathermap for {lat}, {long}}")
#     api_key = get_API_key()
#     open_weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={api_key}&units=imperial"
#     logger.info(f"Calling fetch_from_url for {open_weather_url}")
#     result = await fetch_from_url(open_weather_url, "json")
#     logger.info(f"Data from openweathermap: {result}")
#     temp_F = data["main"]["temp"]
#     return temp_F


# Function to create or overwrite the CSV file with column headings
def init_csv_file(file_path):
    df_empty = pd.DataFrame(
        columns=["Name", "Date", "Test", "Score"]
    )
    df_empty.to_csv(file_path, index=False)


async def update_csv_assessments():
    """Update the CSV file with the latest location information."""
    logger.info("Calling update_csv_location")
    try:
        locations = ["ELY MN", "Death Valley CA", "Maryville MO"]
        #update_interval = 60  # Update every 1 minute (60 seconds)
        #total_runtime = 15 * 60  # Total runtime maximum of 15 minutes
        #num_updates = 10 * len(locations)  # Keep the most recent 10 readings
        #logger.info(f"update_interval: {update_interval}")
        #logger.info(f"total_runtime: {total_runtime}")
        #logger.info(f"num_updates: {num_updates}")

        # Use a deque to store just the last, most recent 10 readings in order
        records_deque = deque(maxlen=None)

        fp = Path(__file__).parent.joinpath("data").joinpath("assessments.csv")

        # Check if the file exists, if not, create it with only the column headings
        if not os.path.exists(fp):
            init_csv_file(fp)

        logger.info(f"Initialized csv file at {fp}")

        for _ in range(num_updates):  # To get num_updates readings
            for location in locations:
                # lat, long = lookup_lat_long(location)
                time_now = datetime.now().strftime("%Y-%m-%d")  # Current time
                new_record = {
                    "Name": location,
                    "Date": time_now,
                    "Test": long,
                    "Score": time_now,
                }
                records_deque.append(new_record)

            # Use the deque to make a DataFrame
            df = pd.DataFrame(records_deque)

            # Save the DataFrame to the CSV file, deleting its contents before writing
            df.to_csv(fp, index=False, mode="w")
            logger.info(f"Saving test score to {fp}")

            # Wait for update_interval seconds before the next reading
            await asyncio.sleep(update_interval)

    except Exception as e:
        logger.error(f"ERROR in update_csv_location: {e}")
