import string

def count_words_in_read_me():
    with open("cs4300/homework1/src/task6_read_me.txt", 'r', encoding='utf-8') as f:
        contents = f.read()
    for mark in string.punctuation:
        contents = contents.replace(mark, "")
    words = contents.split()
    return len(words)

