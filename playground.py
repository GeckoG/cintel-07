import pandas as pd
import csv
from datetime import datetime
from pathlib import Path

fp = Path(__file__).parent.joinpath("data").joinpath("assessments.csv")

name = "matt"
time_now = datetime.now().strftime("%Y-%m-%d")  # Current time
test = "vertical jump"
score = "14"
new_record = [name, time_now, test, score]

with open(fp, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(new_record)
print("Complete")
print(new_record)