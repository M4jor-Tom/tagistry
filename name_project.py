import os
import re
import fileinput
import sys

OLD_STRING = "fastapi_skeleton"

def rename_files_in_directory(directory: str, new_name: str) -> None:
    for root, dirs, files in os.walk(directory):
        if '.git' in dirs:
            dirs.remove('.git')

        for file in files:
            if OLD_STRING in file:
                old_file_path = os.path.join(root, file)
                new_file_name = file.replace(OLD_STRING, new_name)
                new_file_path = os.path.join(root, new_file_name)
                os.rename(old_file_path, new_file_path)


def rename_strings_in_files(directory: str, new_name: str) -> None:
    for root, dirs, files in os.walk(directory):
        if '.git' in dirs:
            dirs.remove('.git')

        for file in files:
            file_path = os.path.join(root, file)
            try:
                with fileinput.FileInput(file_path, inplace=True) as file_input:
                    for line in file_input:
                        print(line.replace(OLD_STRING, new_name), end='')
            except Exception as e:
                print(f"Could not update file {file_path}: {e}")


def delete_script() -> None:
    script_path = os.path.realpath(__file__)
    try:
        os.remove(script_path)
    except Exception as e:
        print(f"Failed to delete script: {e}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <new_name>")
        sys.exit(1)

    new_name: str = sys.argv[1]
    current_directory: str = os.getcwd()

    rename_files_in_directory(current_directory, new_name)
    rename_strings_in_files(current_directory, new_name)

    delete_script()

    print(f"Project named \"{new_name}\"")   


if __name__ == "__main__":
    main()
