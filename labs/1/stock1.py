import csv
import requests

apikey = "TODO"

url = f"https://www.alphavantage.co/query?apikey={apikey}&datatype=csv&function=TIME_SERIES_INTRADAY&interval=1min&symbol=NFLX"
response = requests.get(url)

reader = csv.DictReader(response.text.splitlines())
row = next(reader)
print(row["close"])
