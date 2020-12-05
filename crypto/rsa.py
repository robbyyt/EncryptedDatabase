import warnings
from utilities import is_integer, read_file_into_bytes, gcd, modular_multiplicative_inverse
from sympy.ntheory.generate import randprime
from random import randint


class RSA:
    @staticmethod
    def encrypt_number(message, n, e):
        """
        :param message:
        Integer representing the message that needs to be encrypted
        :param n:
        The RSA public modulus, usually n = pq, where p and q are large primes.
        :param e:
        The RSA public key, chosen so that it is relatively prime to phi(n) = (p-1)(q-1)
        :return:
        The encryption of m using the public key e modulo n: m^e mod n
        """
        if not is_integer(message) or not is_integer(n) or not is_integer(e):
            raise TypeError("Encryption parameters have to be integers")
        if message < 0:
            raise ValueError("RSA can only encrypt non-negative numbers! Message value is not valid: %d" % message)
        if message > n - 1:
            warnings.warn("RSA called with a message larger than n! Output might be unexpected...")
            message = message % n

        return pow(message, e, n)

    @staticmethod
    def decrypt_number(crypt, n, d):
        """
        :param crypt:
        Integer representing the cryptotext that needs to be decrypted
        :param n:
        The RSA public modulus, usually n = pq, where p and q are large primes.
        :param d:
        The RSA private key, chosen so that it is the modular multiplicative inverse modulo phi(n) of e, the public key
        :return:
        """
        if not is_integer(crypt) or not is_integer(n) or not is_integer(d):
            raise TypeError("Decryption parameters have to be integers")
        if crypt < 0:
            raise ValueError("RSA can only encrypt non-negative numbers! Message value is not valid: %d" % crypt)
        if crypt > n - 1:
            raise ValueError("Cannot decrypt values larger than the n modulus!")

        return pow(crypt, d, n)

    @staticmethod
    def encrypt_file(file_path, n, e):
        """
        :param file_path:
        Path of the file that needs to be encrypted.
        :param n:
        RSA public modulus n.
        :param e:
        RSA public key e.
        :return:
        """
        content = read_file_into_bytes(file_path)
        encryption = []
        for b in content:
            encryption.append(RSA.encrypt_number(b, n, e))
        return encryption

    @staticmethod
    def generate_public_key(phi):
        e = randint(2, phi)
        while gcd(phi, e) != 1:
            e = randint(2, phi)
        return e

    @staticmethod
    def generate_rsa_keypair(bit_number=1024):
        p = randprime(2 ** (bit_number / 2 - 1), 2 ** (bit_number / 2))
        q = randprime(2 ** (bit_number / 2 - 1), 2 ** (bit_number / 2))
        phi = (p - 1)*(q - 1)
        e = RSA.generate_public_key(phi)
        d = modular_multiplicative_inverse(e, phi)
        return p * q, e, d
