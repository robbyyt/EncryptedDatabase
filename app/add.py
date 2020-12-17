from database.connection import DBConnection
from crypto.rsa import RSA
from pathlib import Path
import uuid
import os


def add(file_path):
    if not os.path.isfile(file_path):
        raise ValueError("Only files can be added to the database")

    name = Path(file_path).name
    n, e, d = RSA.generate_rsa_keypair()
    fs, chunk_size, enc = RSA.encrypt_file(file_path, n, e)
    uid = str(uuid.uuid4())
    full_name = uid + "_" + name

    save_location = "../encryptions/" + full_name
    with open(save_location, 'w') as f:
        to_write = ""
        for num in enc:
            to_write += str(num)
            to_write += " "

        f.write(to_write)

    conn = DBConnection()
    file_object = {"uid": uid, "name": name, "n": str(n), "e": str(e), "d": str(d),
                   "file_size": str(fs), "chunk_size": str(chunk_size)
                   }
    conn.add_one_file(file_object)
    return True


if __name__ == '__main__':
    add(r"C:\Users\rober\Pictures\bby.jpg")
