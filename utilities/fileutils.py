import os
from math import ceil

def get_file_size(file_path):
    """
    :param file_path:
    Path of the file
    :return:
    Size of the file. (in bytes)
    """
    try:
        return os.path.getsize(file_path)
    except OSError as e:
        print("[get_file_size] Error")
        raise e


def split_into_chunks(source, chunk_size):
    """
    :param source:
    Data source to split. (must be iterable)
    :param chunk_size:
    Chunk size
    :return:
    The source split in chunks of chunk_size elements.
    """
    output = []
    for i in range(0, len(source), chunk_size):
        output.append(source[i: i + chunk_size])

    return output


def read_file_into_bytes(file_path, chunk_size=None):
    """
    :param file_path:
    Path of the file.
    :param chunk_size:
    Optionally, a chunk size.
    :return:
    Returns an array of bytes (or chunks of bytes).
    """
    try:
        with open(file_path, "rb") as f:
            content = f.read()
            if not chunk_size:
                message = bytearray(content)
            else:
                message = split_into_chunks(content, chunk_size)
                message = [int.from_bytes(b, "big") for b in message]

        return message

    except (OSError, IOError) as e:
        print(e.message)
        raise e


def reconstruct_file_content(file_size, chunk_size, content):
    """
    :param file_size:
    Size of the file.
    :param chunk_size:
    Chunk size used for encryption.
    :param content:
    Decrypted content of the file.
    :return:
    Bytes object representing the initial state of the file.
    """
    last_chunk = file_size % chunk_size
    print(last_chunk)
    result = b""
    for i in range(len(content)):
        if i < len(content) - 1:
            result += content[i].to_bytes(chunk_size, 'big')
        elif last_chunk > 0:
            result += content[i].to_bytes(last_chunk, 'big')
        elif last_chunk == 0:
            result += content[i].to_bytes(chunk_size, 'big')

    return result


if __name__ == '__main__':
    file = read_file_into_bytes("../test_files/test.txt")
    printable = [b for b in file]
    print(printable)
    file = read_file_into_bytes("../test_files/test.txt", chunk_size=get_file_size("../test_files/test.txt"))
    printable = [b for b in file]
    print(printable)
    print(get_file_size("../test_files/test.txt"))
