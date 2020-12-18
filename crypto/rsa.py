import warnings
from utilities import is_integer, read_file_into_bytes, gcd, modular_multiplicative_inverse, get_file_size, byte_size
from sympy.ntheory.generate import randprime
from random import randint
from math import ceil


class RSA:
    """
    Encapsulates the method needed for RSA encryption and decryption on numbers and files.
    """
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
        The RSA public modulus, usually n = pq, where p and q are large primes.
        :param e:
        The RSA public key, chosen so that it is relatively prime to phi(n) = (p-1)(q-1)
        :return:
        """
        file_size = get_file_size(file_path)
        n_size = byte_size(n)
        chunks = int(ceil(file_size / n_size))
        content = read_file_into_bytes(file_path, chunk_size=file_size // chunks)

        found_bigger = True
        while found_bigger:
            found_bigger = False
            for b in content:
                if b >= n:
                    found_bigger = True
                    chunks += 1
                    break

        content = read_file_into_bytes(file_path, chunk_size=file_size // chunks)
        encryption = []
        for b in content:
            encryption.append(RSA.encrypt_number(b, n, e))

        return file_size, file_size // chunks, encryption

    @staticmethod
    def decrypt_file_content(content_array, n, d):
        """
        :param content_array:
        Arrat of integers modulo n that need to be decrypted
        :param n:
        The RSA public modulus, usually n = pq, where p and q are large primes.
        :param d:
        The RSA private key, chosen so that it is the modular multiplicative inverse modulo phi(n) of e, the public key
        :return:
        An array formed by decrypting each member of the input parameter.
        """
        plaintext = []
        for b in content_array:
            plaintext.append(RSA.decrypt_number(b, n, d))

        return plaintext

    @staticmethod
    def generate_public_key(phi):
        """
        :param phi:
        The result of applying Euler's totient function on a RSA modulus n
        :return:
        A randomly generated integer modulo phi that is coprime to phi
        """
        e = randint(2, phi)
        while gcd(phi, e) != 1:
            e = randint(2, phi)
        return e

    @staticmethod
    def generate_rsa_keypair(bit_number=1024):
        """
        :param bit_number:
        The number of desired bits for our public modulus n.
        :return:
        n= p * q, e, d, where p and q are prime numbers, and e and d are the public and private exponents.
        """
        p = randprime(2 ** (bit_number / 2 - 1), 2 ** (bit_number / 2))
        q = randprime(2 ** (bit_number / 2 - 1), 2 ** (bit_number / 2))
        phi = (p - 1) * (q - 1)
        e = RSA.generate_public_key(phi)
        d = modular_multiplicative_inverse(e, phi)
        return p * q, e, d
