import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from task6 import count_words_in_read_me

def test_task6_read_me_word_count():
    # I got 104 from copying the text into google docs
    assert count_words_in_read_me() == 104
