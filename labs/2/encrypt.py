while True:
    key = int(input("key: "))
    if key > 0:
        break

plaintext = input("plaintext:  ")

print("ciphertext: ", end="")
for p in plaintext:
    if p.isupper():
        print(chr((ord(p) - ord('A') + key) % 26 + ord('A')), end="")
    elif p.islower():
        print(chr((ord(p) - ord('a') + key) % 26 + ord('a')), end="")
    else:
        print(p, end="")
print()
