from typing import List


def read_numbers() -> List:
    nums = []
    while True:
        number = input("Enter number: ")
        if number.replace(".", "", 1).isdigit():
            nums.append(number)
            continue
        return nums

if __name__ == "__main__":
    print(read_numbers())