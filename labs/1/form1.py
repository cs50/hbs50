import csv

with open("form.csv") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        print(row[1])
