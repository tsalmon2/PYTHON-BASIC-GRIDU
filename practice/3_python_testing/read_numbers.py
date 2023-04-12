"""
It should check successful and failed cases
for example:
If user inputs: 1, 2, 3, 4 -> [1,2,3,4]
If user inputs: 1, 2, Text -> [1,2]

"""
from typing import List

def read_numbers() -> List:
    nums = []
    while True:
        number = input("Enter number: ")
        if number.replace(".", "", 1).isdigit():
            nums.append(int(number))
            continue
        return nums

if __name__ == "__main__":
    print(read_numbers())