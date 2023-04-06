import os
from random import randint
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import time
from multiprocessing import Manager


Path(Path(__file__).parent / "output").mkdir(exist_ok=True)
OUTPUT_DIR = Path(Path(__file__).parent / "output")
RESULT_FILE = Path(OUTPUT_DIR / 'result.csv')

# Overwrite the maximum limit for integer string conversion 
sys.set_int_max_str_digits(9999999)

# def fib(n: int) -> int:
#     """Calculate a value in the Fibonacci sequence by ordinal number"""
#     f0, f1 = 0, 1
#     if n==0: return 0
#     for _ in range(n-1):
#         f0, f1 = f1, f0 + f1
#     return f1

def fib(n: int, memo: dict) -> int:
    if n in memo:
        return memo[n]
    memo[n] = fib(n-1,memo) + fib(n-2,memo)
    return memo[n]

def write_to_file(el: int, memo: dict) -> None:
    """Write the fibonnaci number to a file."""
    with open(Path(OUTPUT_DIR / f"file {el}.txt"), "w", encoding="utf-8") as el_file:
            el_file.write(str(fib(el, memo)))

def func1(array: list, memo: dict) -> None:
    """Concurrently write fibonnaci numbers to files."""
    with ProcessPoolExecutor() as exec: 
        for el in array: exec.submit(write_to_file, el, memo)

def func2(result_folder: str) -> None:
    """Read all files from a folder and write to a csv file."""
    files = os.listdir(result_folder)
    files = [file for file in files if not file.endswith('.csv')]
    if files:
        for file in files:
                with open(Path(result_folder / file), "r", encoding="utf-8") as f, open(RESULT_FILE, "a", encoding="utf-8") as f2:
                    ord_num = file.split(" ")[1].replace('.txt', '')
                    val = f.read()
                    f2.write(f"{ord_num},{val}\n")

if __name__ == '__main__':
    memo = Manager().dict()
    memo[0] = 0
    memo[1] = 1
    start = time.time()
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    # func1(array=[randint(1000, 100000) for _ in range(1000)], memo=memo)
    func1(array=[1,3,5,7,8], memo=memo)
    func2(result_folder=OUTPUT_DIR)
    print(f"time: {time.time() - start}")
