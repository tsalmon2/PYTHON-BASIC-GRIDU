"""
Write tests for 2_python_part_2/task_read_write_2.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
import pytest
import tempfile
import os
from python_part_2 import task_read_write_2 as task

class TestReadWrite2:
    """Class representing TestReadWrite2."""
    def test_read_write_2_reverse(self):
        """Testing that the contents of reversed file are in opposite order to contents of original file."""
        temp_rand_file = tempfile.mkstemp()[1]
        temp_reverse_file = tempfile.mkstemp()[1]
        task.task_read_write_2(temp_rand_file, temp_reverse_file)
        with open(temp_rand_file, "r", encoding="utf-8") as temp_file:
            contents = temp_file.readlines()
        
        with open(temp_reverse_file, "r", encoding="utf-8") as reversed_temp_file:
            reversed_contents = reversed_temp_file.readlines()
        assert reversed_contents == list(reversed(contents))

        os.remove(temp_rand_file)
        os.remove(temp_reverse_file)