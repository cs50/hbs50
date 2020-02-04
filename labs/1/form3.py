import csv

counts = {}

with open("form.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row["title"] not in counts:
            counts[row["title"]] = 0
        else:
            counts[row["title"]] += 1

for title in counts:
    print(title, counts[title])
