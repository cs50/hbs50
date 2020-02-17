import csv

from cs50 import SQL

db = SQL("sqlite:///students.db")

with open("characters.csv") as file:
    reader = csv.DictReader(file)
    for student in reader:
        name = student["name"].split()
        if len(name) == 2:
            first, last = name
            middle = None
        elif len(name) == 3:
            first, middle, last = name
        else:
            continue
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)",
            first, middle, last, student["house"], student["birth"])
        print(f"Added {student['name']} to database.")

