import os
import sys
from functionalities.operations import add, read, delete

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError("Usage: read/add/delete file_path")

    command = sys.argv[1]
    file_path = sys.argv[2]
    cwd = os.getcwd()
    enc_location = cwd + r"\encryptions"
    dec_location = cwd + r"\decryptions"

    if command == "read":
        result = read(file_path, dec_location)
    elif command == "add":
        result = add(file_path, enc_location)
    elif command == "delete":
        result = delete(file_path)
    else:
        result = False

    if result is True:
        print("Success")
    else:
        print("Failure")
