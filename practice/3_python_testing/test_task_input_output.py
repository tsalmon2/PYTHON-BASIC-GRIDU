"""
Write tests for a read_numbers function.
It should check successful and failed cases
for example:
Test if user inputs: 1, 2, 3, 4
Test if user inputs: 1, 2, Text

Tip: for passing custom values to the input() function
Use unittest.mock patch function
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch

TIP: for testing builtin input() function create another function which return input() and mock returned value
"""

from unittest.mock import patch
from read_numbers import read_numbers
import pytest 


class TestInputOutput:
    """Class representing TestInputOutput."""
    @patch('builtins.input', side_effect=['1','2','3','4','text'])
    def test_return_input_nums_text(self, mock_input) -> None:
        assert read_numbers() == [1,2,3,4]

    @patch('builtins.input', side_effect=['text1','text2'])
    def test_read_numbers_with_text_input(self, mock_input) -> None:
        assert read_numbers() == []

