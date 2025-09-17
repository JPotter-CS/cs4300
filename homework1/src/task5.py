def my_favorite_books():
    # My fav books
    books = [
        "Wild at Heart by John Eldredge",
        "How to Win Friends and Influence People by Dale Carnegie",
        "The Four Agreements by Don Miguel Ruiz",
        "The Hobbit by J. R. R. Tolkien"
    ]
    # Using list slicing to store my top 3 books into first_three
    first_three = books[:3]
    # Return list of books and my first three
    return books, first_three

def student_database():
    # Making a dictionary of students. On the left is the ID, on the right is the Student name
    students = {
        1: "Billy Bob",
        2: "Margret",
        3: "Jake",
        4: "Pukeusson"
    }
    # Returns dict of students
    return students
