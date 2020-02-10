import csv
import requests

apikey = "TODO"

symbol = input("Symbol: ")

url = f"https://www.alphavantage.co/query?apikey={apikey}&datatype=csv&function=TIME_SERIES_INTRADAY&interval=1min&symbol={symbol}"
response = requests.get(url)

reader = csv.DictReader(response.text.splitlines())
row = next(reader)
print(row["close"])
