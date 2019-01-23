import cocotb
from cocotb.triggers import ReadOnly
from testlib import *

@cocotb.test(skip=True)
def draw_image(dut):
    yield ReadOnly()

@cocotb.test()
def simple_test(dut):
    ray = VectorSignal(dut.ray)
    center = VectorSignal(dut.center)

    dut.radius.value = fixed_from_float(1)

    ray.assign(make_fvec(0, 0, 1))
    center.assign(make_fvec(0, 1.1, -10))

    yield ReadOnly()

    """
    wire vector_t center_origin;
    wire center_origin_overflow;

    wire fixed_point_t dir_dot;
    wire dir_dot_overflow;

    wire fixed_point_t dir_dot_sq;
    wire dir_dot_sq_overflow;

    wire fixed_point_t center_origin_mag_sq;
    wire center_origin_mag_sq_overflow;

    wire fixed_point_t radius_sq;
    wire radius_sq_overflow;

    wire fixed_point_t discriminant_partial;
    wire discriminant_partial_overflow;

    wire fixed_point_t discriminant;
    wire discriminant_overflow;
    """

    # print(unpack_vector(dut.center_origin.value.integer))
    # print(float_from_fixed(dut.dir_dot.value.integer))
    # print(float_from_fixed(dut.dir_dot_sq.value.integer))
    # print(float_from_fixed(dut.center_origin_mag_sq.value.integer))
    # print(float_from_fixed(dut.discriminant_partial.value.integer))
    # print(float_from_fixed(dut.discriminant.value.integer))

    # print(dut.overflow)

    print(dut.intersection)