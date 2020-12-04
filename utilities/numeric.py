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
