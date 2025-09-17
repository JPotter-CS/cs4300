import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from task4 import calculate_discount

def test_discount_with_integers():
    assert calculate_discount(100, 20) == 80
    assert calculate_discount(150, 10) == 135

def test_discount_with_floats():
    assert calculate_discount(100.0, 15.5) == 84.5
    assert calculate_discount(59.99, 25.0) == 44.9925

def test_discount_mixed_types():
    assert calculate_discount(200, 12.5) == 175.0
    assert calculate_discount(50.5, 10) == 45.45
