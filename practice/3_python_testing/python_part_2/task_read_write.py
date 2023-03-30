"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""
from pathlib import Path


def read_files(*files, res_file_name: str) -> None:
    """Writes comma-separated values from all files to specified file path."""
    files_folder = Path(__file__).parent / "files"
    files_list = [file for file in files]

    # Add contents of each file to results list
    for file in files_list:
        try:
            with open(f"{Path(files_folder / file)}", "r", encoding="utf-8") as f1, open(res_file_name, "a", encoding="utf-8") as f2:
                for line in f1:
                    f2.write(f"{line}, " if file != files_list[-1] else f"{line}")
        except FileNotFoundError:
            raise FileNotFoundError("File doesn't exist. Please recheck file names.")

if __name__ == "__main__":
    read_files("file_1.txt", "file_16.txt", "file_3.txt", res_file_name=f"{Path(__file__).parent / 'files' / 'result.txt'}")