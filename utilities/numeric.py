from utilities.verifications import is_integer
from math import ceil


def byte_size(num):
    """
    :param num:
    Integer input.
    :return:
    The number of bytes needed to represent the input parameter.
    """
    if not is_integer(num):
        raise TypeError("Can't calculate byte size of non-integer!")
    if num == 0:
        return 1
    else:
        bit_number = num.bit_length()
        return ceil(bit_number / 8)


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def modular_multiplicative_inverse(a, modulo):
    x = 0
    x0 = 1
    r = modulo
    r0 = a

    while r0 != 0:
        quotient = r / r0
        x, x0 = x0, x - quotient * x0
        r, r0 = r0, r - quotient * r0

    if r > 1:
        # r > 1 means that input does not have an inverse.
        return False
    if x < 0:
        x += modulo

    return x
