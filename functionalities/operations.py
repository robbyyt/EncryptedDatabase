from database.connection import DBConnection
from crypto.rsa import RSA
from pathlib import Path
from utilities.fileutils import reconstruct_file_content
import uuid
import os


def add(file_path, enc_location):
    """
    :param file_path:
    The path of the file we wish to encrypt.
    :param enc_location:
    The location where we will save the encryption
    :return:
    True, if successful. (if not successful it will raise a ValueError)
    """
    if not os.path.isfile(file_path):
        raise ValueError("Only files can be added to the database")

    name = Path(file_path).name
    n, e, d = RSA.generate_rsa_keypair()
    fs, chunk_size, enc = RSA.encrypt_file(file_path, n, e)
    uid = str(uuid.uuid4())
    full_name = uid + "_" + name

    save_location = enc_location + r"\\" + full_name
    print("SAVING AT: " + save_location)
    with open(save_location, 'w') as f:
        to_write = ""
        for num in enc:
            to_write += str(num)
            to_write += " "

        f.write(to_write)
        f.close()

    conn = DBConnection()
    file_object = {
        "uid": uid,
        "name": name,
        "n": str(n),
        "e": str(e),
        "d": str(d),
        "file_size": str(fs),
        "chunk_size": str(chunk_size)
    }
    conn.add_one_file(file_object)
    return True


def delete(file_path):
    """
    :param file_path:
    The path of the encrypted file that we want to delete from the database.
    :return:
    True, if successful, else False.
    """
    if not os.path.isfile(file_path):
        raise ValueError("Only files can be deleted from the database")

    name = Path(file_path).name
    split_name = name.split("_")
    if len(split_name) != 2:
        raise ValueError("The input file must have a name of type: uid_filename")

    uid, file_name = split_name
    conn = DBConnection()
    files_found = conn.get_file_by_id(uid)

    if len(files_found) == 0:
        print("[Delete]No files found...")
        return False
    elif len(files_found) > 1:
        print("[Delete]Too many matches for uid")
        return False

    file_obj = files_found[0]
    deleted = conn.delete_one_file(file_obj["uid"])
    if deleted == 0:
        print("[Delete]Found nothing to delete")
        return False
    elif deleted > 1:
        print("[Delete]Warning! More than one record deleted!")

    os.remove(file_path)
    return True


def read(file_path, dec_location):
    """
    :param file_path:
    The path to the encrypted file we want to read.
    :param dec_location:
    The location where the decryption will be stored
    :return:
    True if successful, else False.
    """
    if not os.path.isfile(file_path):
        raise ValueError("Only files can be read from the database")

    name = Path(file_path).name
    split_name = name.split("_")
    if len(split_name) != 2:
        raise ValueError("The input file must have a name of type: uid_filename")
    uid, file_name = split_name
    conn = DBConnection()
    files_found = conn.get_file_by_id(uid)

    if len(files_found) == 0:
        print("[Read]No files found...")
        return False
    elif len(files_found) > 1:
        print("[Read]Too many matches for uid")
        return False

    file_obj = files_found[0]
    n = int(file_obj["n"])
    d = int(file_obj["d"])
    file_size = int(file_obj["file_size"])
    chunk_size = int(file_obj["chunk_size"])

    with open(file_path, 'r') as f:
        content = f.read()
        content = content.split(" ")
        content.pop()
        content = [int(i) for i in content]
        f.close()

    decryption = RSA.decrypt_file_content(content, n, d)
    file_content = reconstruct_file_content(file_size, chunk_size, decryption)
    save_location = dec_location + r"\\" + file_name
    print("READING INTO: " + save_location)
    with open(save_location, 'wb') as f:
        f.write(file_content)
        f.close()

    return True
