while True:
    height = int(input("Height: "))
    if height > 0:
        break

for i in range(height):
    for j in range(height - i - 1):
        print(" ", end="")
    for j in range(i + 1):
        print("#", end="")
    print()
