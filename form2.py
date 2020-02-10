import csv

with open("form.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row["title"])
