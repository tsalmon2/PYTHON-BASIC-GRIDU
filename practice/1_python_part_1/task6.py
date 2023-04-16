"""
Write function which receives filename and reads file line by line and returns min and mix integer from file.
Restriction: filename always valid, each line of file contains valid integer value
Examples:
    # file contains following lines:
        10
        -2
        0
        34
    >>> get_min_max('filename')
    (-2, 34)

Hint:
To read file line-by-line you can use this:
with open(filename) as opened_file:
    for line in opened_file:
        ...
"""
from typing import Tuple
from math import inf 

def get_min_max(filename:str) -> Tuple[int, int]:
    """Returns the minimum and maximum integers contained in the file"""
    
    # Initializing max and min to a low and high value respectively.
    max = -inf
    min = inf

    # Looping through lines in the file and comparing to current min/max.
    with open(filename, "r") as f:
        for num in f:
            num = int(num.rstrip())
            if num > max:
                max = num
            if num < min:
                min = num
    return (min, max)