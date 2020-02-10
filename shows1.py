import csv

title = input("Title: ")

with open("shows.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row["primaryTitle"] == title:
            print(row["primaryTitle"], row["startYear"])
