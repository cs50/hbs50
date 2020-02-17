import csv

from cs50 import SQL

db = SQL("sqlite:///students.db")

house = input("House: ")
people = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", house)
for person in people:
    name = []
    for field in ["first", "middle", "last"]:
        if person[field]:
            name.append(person[field])
    name = " ".join(name)
    print(f"{name}, born {person['birth']}")
