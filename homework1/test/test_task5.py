import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from task5 import my_favorite_books, student_database

def test_books_full_and_slice():
    books, first_three = my_favorite_books()
    assert books[0] == "Wild at Heart by John Eldredge"
    assert books[2] == "The Four Agreements by Don Miguel Ruiz"
    assert first_three == books[:3]
    assert len(first_three) == 3

def test_student_dict_contents():
    students = student_database()
    assert students[1] == "Billy Bob"
    assert students[2] == "Margret"
    assert students[3] == "Jake"
    assert students[4] == "Pukeusson"
    assert set(students.values()) == {"Billy Bob", "Margret", "Jake", "Pukeusson"}
