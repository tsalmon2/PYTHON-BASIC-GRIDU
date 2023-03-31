"""
Write test for print_name_address function
Use Mock for mocking args argument https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 123
    >>> m.method()
    123
"""

import pytest
from unittest.mock import Mock, patch
from task_4 import get_args, argparse

from task_4_exceptions import InvalidFakerProviderException, InvalidKeyValuePairException

@patch('argparse.ArgumentParser')
class TestPrintName:
    # argparse.ArgumentParser(name).add_argument()
    def test_with_valid_args(self, arg_mock, capfd):
        add_argument = Mock()
        add_argument.side_effect = [5, '--name=name', '--addr=address']
        arg_mock.return_value = add_argument
        assert arg_mock() == 'j'
        # assert add_argument() == 5
        # assert add_argument() == 'h'
        # assert add_argument() == 'i'

        # captured = capfd.readouterr()
   

