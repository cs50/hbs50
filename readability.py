def main():

    s = input("Text: ")

    letters = count_letters(s)
    sentences = count_sentences(s)
    words = count_words(s)

    coleman = round(0.0588 * (100 * letters / words)
                    - 0.296 * (100 * sentences / words)
                    - 15.8)

    if coleman >= 16:
        print("Grade 16+")
    elif coleman < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {coleman}")

def count_letters(text):
    count = 0
    for character in text:
        if character.isalpha():
            count += 1
    return count

def count_sentences(text):
    count = 0
    for character in text:
        if character == "." or character == "!" or character == "?":
            count += 1
    return count

def count_words(text):
    return len(text.split())

main()
