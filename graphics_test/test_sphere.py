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

    dut.radius.value = fixed_from_float(1.75)

    ray.assign(make_fvec(-0.7530517578125, 0.4705810546875, 0.458984375))
    center.assign(make_fvec(0, 0, 2))

    yield ReadOnly()

    print(dut.intersection)