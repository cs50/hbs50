import csv
import requests

apikey = "TODO"

symbol = input("Symbol: ")
buy_date = input("Bought: ")
sell_date = input("Sold: ")

url = f"https://www.alphavantage.co/query?apikey={apikey}&datatype=csv&function=TIME_SERIES_DAILY&interval=1min&symbol={symbol}"
response = requests.get(url)

reader = csv.DictReader(response.text.splitlines())
for row in reader:
    if row["timestamp"] == buy_date:
        buy_price = float(row["close"])
    elif row["timestamp"] == sell_date:
        sell_price = float(row["close"])

print((sell_price / buy_price - 1.0) * 100)
