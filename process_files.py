import os
import sys
import fnmatch
from pathlib import Path
from typing import List, Set

def parse_gitignore(gitignore_path: str) -> List[str]:
    """
    Parse the .gitignore file and return a list of ignore patterns.

    Args:
        gitignore_path (str): Path to the .gitignore file.

    Returns:
        List[str]: List of ignore patterns.
    """
    try:
        with open(gitignore_path, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except IOError:
        print(f"Warning: Unable to read .gitignore file at {gitignore_path}")
        return []

def should_ignore(file_path: str, ignore_patterns: List[str]) -> bool:
    """
    Check if a file should be ignored based on the ignore patterns.

    Args:
        file_path (str): Path of the file to check.
        ignore_patterns (List[str]): List of ignore patterns.

    Returns:
        bool: True if the file should be ignored, False otherwise.
    """
    for pattern in ignore_patterns:
        if pattern.endswith('/'):
            if fnmatch.fnmatch(file_path, f"{pattern}*"):
                return True
        elif fnmatch.fnmatch(file_path, pattern):
            return True
    return False

def process_file(file_path: str, output_file) -> None:
    """
    Process a single file and write its contents to the output file.

    Args:
        file_path (str): Path of the file to process.
        output_file: File object to write the output to.
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
    output_file.write("\n" + "-" * 40 + "\n")

def sort_items(items: List[str]) -> List[str]:
    """
    Sort items alphabetically with hidden files appearing first.

    Args:
        items (List[str]): List of file or directory names.

    Returns:
        List[str]: Sorted list of items.
    """
    return sorted(items, key=lambda x: (not x.startswith('.'), x.lower()))

def process_directory(directory_path: str, output_file, ignore_patterns: List[str], include_git: bool = False, recursive: bool = True) -> None:
    """
    Process files and subdirectories within a directory.

    Args:
        directory_path (str): Path to the directory to process.
        output_file: File object to write the output to.
        ignore_patterns (List[str]): List of ignore patterns.
        include_git (bool): Whether to include the .git folder. Defaults to False.
        recursive (bool): Whether to process subdirectories recursively. Defaults to True.
    """
    if recursive:
        for root, dirs, files in os.walk(directory_path):
            if not include_git and '.git' in dirs:
                dirs.remove('.git')

            # Sort directories and files
            dirs[:] = sort_items(dirs)
            files = sort_items(files)

            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, directory_path)
                
                if not should_ignore(rel_path, ignore_patterns):
                    process_file(file_path, output_file)

            # Remove ignored directories to prevent os.walk from traversing them
            dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), ignore_patterns)]
    else:
        items = sort_items(os.listdir(directory_path))
        for item in items:
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                if not should_ignore(item, ignore_patterns):
                    process_file(item_path, output_file)

def main():
    """
    Main function to process the specified path and write the output to a file.
    """
    if len(sys.argv) < 3:
        print("Usage: python3 process_files.py <path> <output_file> [.gitignore_path] [--include-git] [--no-recursive]")
        sys.exit(1)

    path = sys.argv[1]
    output_file_path = sys.argv[2]
    args = sys.argv[3:]

    gitignore_path = next((arg for arg in args if arg.endswith('.gitignore')), None)
    include_git = '--include-git' in args
    recursive = '--no-recursive' not in args

    ignore_patterns = parse_gitignore(gitignore_path) if gitignore_path else []

    with open(output_file_path, "w") as output_file:
        if os.path.isfile(path):
            process_file(path, output_file)
        elif os.path.isdir(path):
            process_directory(path, output_file, ignore_patterns, include_git, recursive)
        else:
            print(f"Error: Invalid path: {path}")
            sys.exit(1)

if __name__ == "__main__":
    main()