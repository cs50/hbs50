while True:
    dollars = float(input("Change: "))
    if dollars > 0.0:
        break

cents = round(dollars * 100)

coins = 0

while cents >= 25:
    coins += 1
    cents -= 25

while cents >= 10:
    coins += 1
    cents -= 10

while cents >= 5:
    coins += 1
    cents -= 5

while cents >= 1:
    coins += 1
    cents -= 1

print(coins)
