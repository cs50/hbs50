import csv

genre = input("Genre: ")

with open("shows.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        for g in row["genres"].split(","):
            if genre.lower() == g.lower():
                print(row["primaryTitle"])
