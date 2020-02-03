while True:
    size = int(input("Size: "))
    if size > 0:
        break

for i in range(size):
    for j in range(size):
        print("#", end="")
    print()
