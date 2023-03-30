"""
Write a parametrized test for two functions.
The functions are used to find a number by ordinal in the Fibonacci sequence.
One of them has a bug.

Fibonacci sequence: https://en.wikipedia.org/wiki/Fibonacci_number

Task:
 1. Write a test with @pytest.mark.parametrize decorator.
 2. Find the buggy function and fix it.
"""
import pytest


def fibonacci_1(n: int) -> int:
    a, b = 0, 1
    nums_lst = [0,1]
    for _ in range(n-1):
        a, b = b, a + b
        nums_lst.append(b)
    return b

def fibonacci_2(n: int) -> int:
    fibo = [0, 1]
    for i in range(1, n+1):
        fibo.append(fibo[i-1] + fibo[i-2])
    return fibo[n]

def bug_fix_fibonacci_2(n: int) -> int: # The fix for fibonacci_2 is to start i at 2 instead of 1 so that it corresponds with the index
    fibo = [0, 1]
    for i in range(2, n+1):
        fibo.append(fibo[i-1] + fibo[i-2])
    print(fibo)
    return fibo[n]

def fix_fibonacci_1(n: int) -> int: # To return the correct value when n is 0, add a conditional statement before the loop
    a, b = 0, 1
    nums_lst = [0,1]
    if n == 0: return 0
    for _ in range(n-1):
        a, b = b, a + b
        nums_lst.append(b)
    return b


class TestParametrize:
    """Class representing TestParametrize."""
    @pytest.mark.parametrize("func", [fibonacci_1, fibonacci_2])
    @pytest.mark.parametrize("pos,val", [(0,0), (1,1), (2,1), (3,2), (5,5), (6,8), (19,4181)])
    def test_original_fibonnaci(self, func, pos, val):
        """Testing return values of the two functions for a range of numbers."""
        assert func(pos) == val

    @pytest.mark.parametrize("func", [fix_fibonacci_1, bug_fix_fibonacci_2])
    @pytest.mark.parametrize("pos,val", [(0,0), (1,1), (2,1), (3,2), (5,5), (6,8), (19,4181)])
    def test_fixed_fibonnaci(self, func, pos, val):
        """Testing return values of the two fixed functions for a range of numbers."""
        assert func(pos) == val

    '''fibonacci_2 failed 4/7 test cases so it is the buggy function 
    but fibonnacci_1 failed on 0 because it returns 1 for the 0th value 
    instead of 0.

    The fixed functions passed all test cases.
    '''