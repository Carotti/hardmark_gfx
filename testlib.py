
import random

integer_w = 19
fraction_w = 13
fixed_w = integer_w + fraction_w

def bitmask(width):
    return (1 << width) - 1

def unpack_if(n):
    return (n >> fraction_w) & bitmask(integer_w), n & bitmask(fraction_w)

def pack_if(if_value):
    i, f = if_value
    return ((i << fraction_w) & (bitmask(integer_w) << fraction_w)) | (f & bitmask(fraction_w))

def pack_vector(x, y, z):
    return (x << (fixed_w * 2)) | (y << fixed_w) | z

def unpack_vector(v):
    x = v >> (fixed_w * 2)
    y = (v >> (fixed_w)) & bitmask(fixed_w)
    z = v & bitmask(fixed_w)
    return x, y, z

def is_negative(n):
    return (n & (1 << (fixed_w - 1))) != 0

def random_op():
    return random.randint(0, 2 ** (fixed_w - 1))

def fixed_from_float(n):
    if n < 0:
        n = -n
        negative = True
    else:
        negative = False

    result = int(n * (1 << fraction_w))

    if negative:
        return (result ^ bitmask(fixed_w)) + 1
    else:
        return result

def float_from_fixed(n):
    n &= bitmask(fixed_w)
    negative = n & (1 << (fixed_w - 1))

    if negative:
        n = (n ^ bitmask(fixed_w)) + 1

    result = (float)(n) / (float)(1 << fraction_w)

    return -result if negative else result