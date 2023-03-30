"""
Write tests for 2_python_part_2/task_read_write.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
import tempfile
import pytest
import os
from python_part_2 import task_read_write as task


class TestReadWrite:
    """Class representing TestReadWrite."""
    def test_read_write_output(self):
        """Testing that output is 80, 37."""
        temp_path = tempfile.mkstemp()[1]
        task.read_files("file_1.txt", "file_2.txt", res_file_name=temp_path)
        with open(temp_path, "r", encoding="utf-8") as temp_file:
            contents = temp_file.read()
        os.remove(temp_path)
        assert contents == "80, 37"

    def test_invalid_filename(self):   
        """Testing that FileNotFoundError is thrown with invalid filename.""" 
        temp_path = tempfile.mkstemp()[1]
        with pytest.raises(FileNotFoundError, match=r"File doesn't exist. Please recheck file names."):
            task.read_files("file_1.txt", "files_2.txt", res_file_name=temp_path)
        os.remove(temp_path)