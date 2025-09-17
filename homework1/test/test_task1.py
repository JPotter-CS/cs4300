import sys
import os
import pytest

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import directly from task1 (since src is now in path)
from task1 import hello_world

def test_hello_world_output(capsys):
    hello_world()
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"
