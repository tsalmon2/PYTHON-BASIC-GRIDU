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
    def test_with_valid_args(self, fake_mock, arg_mock, capfd):
        mock = Mock()
        mock.name.return_value = 'Amanda Tracy'
        mock.address.return_value = '944 Priscilla Junctions Suite 591\nEast Davidberg, NV 13114'
        fake_mock.return_value = mock
        args = arg_mock()
        print_name_address(args) 
        out_dict = "{'name': 'Amanda Tracy', 'addr': '944 Priscilla Junctions Suite 591\\nEast Davidberg, NV 13114'}"
        captured = capfd.readouterr()
        assert captured.out  == f"{out_dict}\n"*4

    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(NUMBER=4, add_args=['--name=name', 'addr=address=add']))
    def test_with_invalid_args(self, arg_mock):
        args = arg_mock()
        with pytest.raises(InvalidKeyValuePairException):
            print_name_address(args) 

    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(NUMBER=4, add_args=['--height=height', 'addr=address']))
    def test_with_invalid_faker_attrs(self, arg_mock):
        args = arg_mock()
        with pytest.raises(InvalidFakerProviderException):
            print_name_address(args) 
