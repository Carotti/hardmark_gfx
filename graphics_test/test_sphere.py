import cocotb
from cocotb.triggers import ReadOnly
from testlib import *

@cocotb.test()
def simple_test(dut):
    origin = VectorSignal(dut.view_origin)
    direction = VectorSignal(dut.view_direction)
    center = VectorSignal(dut.center)

    dut.radius.value = fixed_from_float(1)

    origin.assign(make_fvec(0, 0, 0))
    direction.assign(make_fvec(0, 0, 1))
    center.assign(make_fvec(0, 0, 10))

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

    print(dut.dir_dot)

    print(dut.dir_dot_sq_overflow)
    print(dut.center_origin_mag_sq_overflow)
    print(dut.intersection)