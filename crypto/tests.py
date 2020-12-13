from crypto import RSA
from utilities import reconstruct_file_content

if __name__ == '__main__':
    print("RSA sample usage")
    n, e, d = RSA.generate_rsa_keypair()
    fs, chunk_size, enc = RSA.encrypt_file("../test_files/test.txt", n, e)
    dec = RSA.decrypt_file_content(enc, n, d)
    print("Encryption: " + str(enc))
    print("File size: " + str(fs) + " " + "Chunk size: " + str(chunk_size))
    print("Decryption: " + str(dec))
    print("File content: " + str(reconstruct_file_content(fs, chunk_size, dec)))
