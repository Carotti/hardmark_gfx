
import random

integer_w = 19
fraction_w = 13
fixed_w = integer_w + fraction_w

VEC_X = 0
VEC_Y = 1
VEC_Z = 2

VEC_DIRS = [VEC_X, VEC_Y, VEC_Z]

class VectorSignal:
    def __init__(self, handle):
        self.handle = handle

    def assign_xyz(self, x, y, z):
        self.handle.value = pack_vector(x, y, z)

    def assign(self, v):
        x, y, z = v
        self.assign_xyz(x, y , z)

def bitmask(width):
    return (1 << width) - 1

def unpack_if(n):
    return (n >> fraction_w) & bitmask(integer_w), n & bitmask(fraction_w)

def pack_if(if_value):
    i, f = if_value
    return ((i << fraction_w) & (bitmask(integer_w) << fraction_w)) | (f & bitmask(fraction_w))

def pack_vector(x, y, z):
    return ((x & bitmask(fixed_w)) << (fixed_w * 2)) | ((y & bitmask(fixed_w)) << fixed_w) | (z & bitmask(fixed_w))

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

def make_fvec(x, y, z):
    return fixed_from_float(x), fixed_from_float(y), fixed_from_float(z)

def make_fvec_packed(x, y, z):
    xn, yn, zn = make_fvec(x, y, z)
    return pack_vector(xn, yn, zn)

def add_operation(op1, op2):
    result = (op1 + op2) & bitmask(fixed_w)

    op1_sign = is_negative(op1)
    op2_sign = is_negative(op2)
    result_sign = is_negative(result)

    if (op1_sign == op2_sign and result_sign != op1_sign):
        overflow = 1
    else:
        overflow = 0

    return result, overflow

def twos_complement_negate(x, width):
    return (x ^ bitmask(width)) + 1

def signed_mul(op1, op2):
    op1_sign = is_negative(op1)
    op2_sign = is_negative(op2)

    if op1_sign:
        op1 = twos_complement_negate(op1, fixed_w)
    
    if op2_sign:
        op2 = twos_complement_negate(op2, fixed_w)

    result = op1 * op2

    result_sign = result & (1 << 2 * fixed_w - 1)

    if (op1_sign != op2_sign) != result_sign:
        result = twos_complement_negate(result, 2 * fixed_w)

    return result

def mul_operation(op1, op2):
    op1_sign = is_negative(op1)
    op2_sign = is_negative(op2)

    result = signed_mul(op1, op2)

    result_sign = ((result >> (fixed_w + fraction_w)) == bitmask(integer_w))
    result_overflow = (result >> (fixed_w + fraction_w)) != 0 and not result_sign
    result = (result >> fraction_w) & bitmask(fixed_w)

    if (((op1_sign != op2_sign) != result_sign) and result != 0) | result_overflow:
        overflow = 1
    else:
        overflow = 0

    return result, overflow

def sub_operation(op1, op2):
    result = (op1 - op2) & bitmask(fixed_w)

    op1_sign = is_negative(op1)
    op2_sign = is_negative(op2)
    result_sign = is_negative(result)

    if (op1_sign != op2_sign and result_sign == op2_sign):
        overflow = 1
    else:
        overflow = 0

    return result, overflow

def scalar_mul_operation(s, v):
    x, y, z = unpack_vector(v)
    x_new, ox = mul_operation(s, x)
    y_new, oy = mul_operation(s, y)
    z_new, oz = mul_operation(s, z)
    return pack_vector(x_new, y_new, z_new), ox | oy | oz

def dot_product_operation(v1, v2):
    x1, y1, z1 = unpack_vector(v1)
    x2, y2, z2 = unpack_vector(v2)

    xs, xo = mul_operation(x1, x2)
    ys, yo = mul_operation(y1, y2)
    zs, zo = mul_operation(z1, z2)

    xys, xyo = add_operation(xs, ys)

    xyzs, xyzo = add_operation(xys, zs)

    return xyzs, xo | yo | zo | xyo | xyzo

def normalize_vector_operation(v):
    scalar = 0
    for bit in range(fixed_w - 2, -1, -1):
        magnitude = 1 << bit
        scaled_vec, scale_overflow = scalar_mul_operation(scalar | magnitude, v)
        dot_product, dot_overflow = dot_product_operation(scaled_vec, scaled_vec)
        if not scale_overflow and not dot_overflow:
            if dot_product <= fixed_from_float(1):
                scalar += magnitude
    scaled_vec, scale_overflow = scalar_mul_operation(scalar, v)
    if scale_overflow:
        raise ValueError("That shouldn't happen!")
    return scaled_vec

def make_normalize_test(x, y, z):
    v = pack_vector(*tuple(map(fixed_from_float, (x, y, z))))
    result = unpack_vector(normalize_vector_operation(v))
    x, y, z = tuple(float_from_fixed(i) for i in result)
    print(x ** 2 + y ** 2 + z ** 2)
    return x, y, z