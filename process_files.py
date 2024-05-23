import os
import sys
from pathlib import Path

def process_file(file_path, output_file):
    """
    Writes the file path and its contents to the output file.

    Args:
        file_path (str): The path to the file.
        output_file (TextIOWrapper): The file object to write the output to.
    """
    output_file.write(f"File: {file_path}\n")
    try:
        with open(file_path, "rb") as file:
            content = file.read()
            try:
                content = content.decode("utf-8")
                output_file.write(content)
            except UnicodeDecodeError:
                output_file.write("[Binary or unsupported file content]\n")
    except IOError:
        output_file.write("[Error reading file]\n")
    finally:
        output_file.write("\n" + "-" * 40 + "\n")  # Separator between files

def process_directory(directory_path, output_file, gitignore_path=None):
    """
    Recursively processes files and subdirectories within a directory.

    Args:
        directory_path (str): The path to the directory.
        output_file (TextIOWrapper): The file object to write the output to.
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
            process_file(item_path, output_file)
        elif os.path.isdir(item_path):
            process_directory(item_path, output_file, gitignore_path)

def main():
    """
    Main function to process the specified path and write the output to a file.
    """
    if len(sys.argv) < 3:
        print("Please provide a path and an output file as arguments.")
        sys.exit(1)

    path = sys.argv[1]
    output_file_path = sys.argv[2]
    gitignore_path = None

    if len(sys.argv) > 3:
        gitignore_path = sys.argv[3]

    with open(output_file_path, "w") as output_file:
        if os.path.isfile(path):
            process_file(path, output_file)
        elif os.path.isdir(path):
            process_directory(path, output_file, gitignore_path)
        else:
            print(f"Invalid path: {path}")
            sys.exit(1)

if __name__ == "__main__":
    main()