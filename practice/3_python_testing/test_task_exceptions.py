"""
Write tests for division() function in 2_python_part_2/task_exceptions.py
In case (1,1) it should check if exception were raised
In case (1,0) it should check if return value is None and "Division by 0" printed
If other cases it should check if division is correct

TIP: to test output of print() function use capfd fixture
https://stackoverflow.com/a/20507769
"""
import pytest 
from python_part_2 import task_exceptions as task


class TestExceptions:
    """Class representing TestExceptions."""
    def test_division_ok(self):
        """Testing division with valid integers returns correct result."""
        assert task.division(18,2) == 9

    def test_division_by_zero_return(self):
        """Testing division by 0 returns None."""
        assert task.division(18,0) is None

    def test_division_by_one(self):
        """Testing division by 1 raises custom DivisionByOneException."""
        with pytest.raises(task.DivisionByOneException):
            task.division(18,1)

    @pytest.mark.parametrize("callable", [(18,2), (18,1)])
    def test_division_output(self, capfd, callable):
        """Testing division by valid integer or 1 prints 'Division finished'."""
        try:
            task.division(*callable)
        except(task.DivisionByOneException):
            pass
        finally:
            captured = capfd.readouterr()
            assert captured.out == "Division finished\n"
        
    def test_division_by_zero_stmt(self, capfd):
        """Testing division by 0 prints "Division by 0" and 'Division finished'."""
        task.division(18,0)
        captured = capfd.readouterr()
        assert captured.out == "Division by 0\nDivision finished\n"
