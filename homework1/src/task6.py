import string

def count_words_in_read_me():
    # Open read me file for reading (r)
    with open("cs4300/homework1/src/task6_read_me.txt", 'r', encoding='utf-8') as f:
        # Store data in file into contents
        contents = f.read()
    # For mark (comma, period, etc) in string
    for mark in string.punctuation:
        # Removes any marks from contents
        contents = contents.replace(mark, "")
    # Splitting content at white space to determine amount of words and storing in a list "words"
    words = contents.split()
    # Return amount of words (words is a list)
    return len(words)

