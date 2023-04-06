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
from task_4 import get_args, argparse, print_name_address, faker

from task_4_exceptions import InvalidFakerProviderException, InvalidKeyValuePairException

class TestPrintName:
    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(NUMBER=4, add_args=['--name=name', 'addr=address']))
    @patch('faker.Faker')
    def test_with_valid_args_2(self, fake_mock, arg_mock, capfd):
        fake_mock.name.return_value = 'Amanda Tracy'
        fake_mock.address.return_value = '944 Priscilla Junctions Suite 591\nEast Davidberg, NV 13114'
        # assert getattr(fake_mock, 'name') == 'd'

        args = arg_mock()
        print_name_address(args) 
        captured = capfd.readouterr()
        # assert captured.out == ''


