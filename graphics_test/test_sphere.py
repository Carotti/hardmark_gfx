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

    dut.radius.value = fixed_from_float(0.0)

    ray.assign(make_fvec(0, 0.1, 0.9))
    center.assign(make_fvec(0, 0, 2))

    yield ReadOnly()

    print(dut.intersection)

    print(dut.overflow)
    print(float_from_fixed(dut.discriminant_partial.value.integer))
    print(float_from_fixed(dut.dir_dot_sq.value.integer))