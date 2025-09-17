import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from task2 import variables

def test_integer():
    # Only take a from variables return
    a, *_ = variables()
    assert isinstance(a, int)
    assert a == 3

def test_float():
    # Only take b,c from variables return
    _, b, c, *_ = variables()
    assert isinstance(b, float)
    assert b == 3.33
    assert c == 6.33

def test_string():
    # Only take string from variables return
    *_, string, _, _, _, _, _ = variables()
    assert isinstance(string, str)
    assert string == "Hi :)"

def test_booleans():
    # Only take bools and res from variables return
    *_, bool_a, bool_b, res1, res2, res3 = variables()
    assert isinstance(bool_a, bool)
    assert isinstance(bool_b, bool)
    assert res1 is True
    assert res2 is False
    assert res3 is False
