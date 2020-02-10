plaintext = input("ciphertext: ")

for key in range(1, 26):
    print("plaintext:  ", end="")
    for p in plaintext:
        if p.isupper():
            print(chr((ord(p) - ord('A') + key) % 26 + ord('A')), end="")
        elif p.islower():
            print(chr((ord(p) - ord('a') + key) % 26 + ord('a')), end="")
        else:
            print(p, end="")
    print()
