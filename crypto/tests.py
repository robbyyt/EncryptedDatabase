from crypto import RSA

if __name__ == '__main__':
    print("RSA sample usage")
    n, e, d = RSA.generate_rsa_keypair()
    enc = RSA.encrypt_file("../test_files/test.txt", n, e)
    print(enc)
