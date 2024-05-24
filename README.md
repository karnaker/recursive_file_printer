# File Content Extractor

The File Content Extractor is a Python script that allows you to process files and directories, extracting the contents of each file and writing them to an output file. It provides various options to customize the processing behavior, such as recursively processing subdirectories, using a custom .gitignore file, and including or excluding the .git folder.

## Features

* Process a single file or a directory recursively
* Write the file paths and contents to an output file
* Handle binary and unsupported file formats gracefully
* Use a custom .gitignore file to exclude specific files or folders
* Include or exclude the .git folder from processing
* Option to process only files in the current directory (non-recursive)

## Requirements

Python 3.x

## Usage

`python3 process_files.py <path> <output_file> [options]`

* `<path>`: The path to the file or directory to process.
* `<output_file>`: The path to the output file where the extracted contents will be written.
* [options]:
  * `/path/to/.gitignore`: Specify a custom .gitignore file to use for excluding files or folders.
  * `--include-git`: Include the .git folder in the processing (default: exclude .git).
  * `--no-recursive`: Process only files in the current directory, ignoring subdirectories (default: recursive processing).

## Example usage:

1. Process a single file and write the output to output.txt
    ```sh
    python3 process_files.py /path/to/file.txt output.txt
    ```

2. Process a directory recursively and write the output to output.txt
    ```sh
    python3 process_files.py /path/to/directory output.txt
    ```

3. Process a directory non-recursively (only files in the current directory) and write the output to output.txt
    ```sh
    python3 process_files.py /path/to/directory output.txt --no-recursive
    ```

4. Process a directory recursively, use a custom .gitignore file, and write the output to output.txt
    ```sh
    python3 process_files.py /path/to/directory output.txt /path/to/.gitignore
    ```

5. Process a directory non-recursively, use a custom .gitignore file, and write the output to output.txt
    ```sh
    python3 process_files.py /path/to/directory output.txt /path/to/.gitignore --no-recursive
    ```

6. Process a directory recursively, include the .git folder, and write the output to output.txt
    ```sh
    python3 process_files.py /path/to/directory output.txt --include-git
    ```

7. Process a directory non-recursively, include the .git folder, and write the output to output.txt
    ```sh
    python3 process_files.py /path/to/directory output.txt --include-git --no-recursive
    ```

8. Process a directory recursively, use a custom .gitignore file, include the .git folder, and write the output to output.txt
    ```sh
    python3 process_files.py /path/to/directory output.txt /path/to/.gitignore --include-git
    ```

9. Process a directory non-recursively, use a custom .gitignore file, include the .git folder, and write the output to output.txt
    ```sh
    python3 process_files.py /path/to/directory output.txt /path/to/.gitignore --include-git --no-recursive
    ```

## How It Works

The script follows these steps:
1. Parse the command-line arguments to determine the path to process, the output file, and any additional options.
1. If the provided path is a file, process the file and write its contents to the output file.
1. If the provided path is a directory, process the directory based on the specified options:
  * If a custom .gitignore file is provided, use it to exclude files or folders.
  * If --include-git is specified, include the .git folder in the processing.
  * If --no-recursive is not specified, recursively process subdirectories.
1. For each file encountered, write the file path and its contents to the output file.
  * If the file is binary or unsupported, write a message indicating so.
  * If an error occurs while reading the file, write an error message.
1. Repeat the process for all files and directories based on the specified options.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.