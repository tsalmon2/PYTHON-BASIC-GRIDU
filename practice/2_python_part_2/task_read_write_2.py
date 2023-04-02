"""
Use function 'generate_words' to generate random words.
Write them to a new file encoded in UTF-8. Separator - '\n'.
Write second file encoded in CP1252, reverse words order. Separator - ','.

Example:
    Input: ['abc', 'def', 'xyz']

    Output:
        file1.txt (content: "abc\ndef\nxyz", encoding: UTF-8)
        file2.txt (content: "xyz,def,abc", encoding: CP1252)
"""
from typing import List
from pathlib import Path


def generate_words(n: int=20) -> List:
    """Generates a list of random words of specified size."""
    import string
    import random

    words = list()
    for _ in range(n):
        word = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
        words.append(word)

    return words

def task_read_write_2(rand_file_name: str, reverse_file_name: str) -> None:
    """Writes random words and reverse of words to separate files."""
    Path(Path(__file__).parent / "rand_files").mkdir(exist_ok=True)
    rand_words_folder = Path(__file__).parent / "rand_files"
    rand_words = generate_words(10)

    with open(Path(rand_words_folder / rand_file_name), "w", encoding="utf-8") as f:
        f.writelines(word + '\n' for word in rand_words)

    with open(Path(rand_words_folder / reverse_file_name), "w", encoding="CP1252") as f2:
        f2.writelines(word + '\n' for word in rand_words[::-1])

if __name__ == '__main__':
    task_read_write_2("random_words.txt", "reverse_words.txt")
