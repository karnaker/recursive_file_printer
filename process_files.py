import os
import sys
from pathlib import Path

def process_file(file_path):
    """
    Prints the file path and its contents.

    Args:
        file_path (str): The path to the file.
    """
    print(f"File: {file_path}")
    with open(file_path, "r") as file:
        content = file.read()
        print(content)
        print("-" * 40)  # Separator between files

def process_directory(directory_path, gitignore_path=None):
    """
    Recursively processes files and subdirectories within a directory.

    Args:
        directory_path (str): The path to the directory.
        gitignore_path (str, optional): The path to the .gitignore file. Defaults to None.
    """
    gitignore = None
    if gitignore_path:
        with open(gitignore_path, "r") as file:
            gitignore = file.read().splitlines()

    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)

        if gitignore and item in gitignore:
            continue

        if os.path.isfile(item_path):
            process_file(item_path)
        elif os.path.isdir(item_path):
            process_directory(item_path, gitignore_path)

def main():
    """
    Main function to process the specified path.
    """
    if len(sys.argv) < 2:
        print("Please provide a path as an argument.")
        sys.exit(1)

    path = sys.argv[1]
    gitignore_path = None

    if len(sys.argv) > 2:
        gitignore_path = sys.argv[2]

    if os.path.isfile(path):
        process_file(path)
    elif os.path.isdir(path):
        process_directory(path, gitignore_path)
    else:
        print(f"Invalid path: {path}")
        sys.exit(1)

if __name__ == "__main__":
    main()