from . import *

import cocotb
from cocotb.triggers import RisingEdge, ReadOnly
from cocotb.clock import Clock
from testlib import *

@cocotb.test()
def normalize_test(dut):
    cocotb.fork(Clock(dut.clk, 1, units="ns").start())

    op = VectorSignal(dut.op)
    op.assign(make_fvec(4.1, 3.1, 15))

    yield ReadOnly()

    for _ in range(fixed_w):
        yield RisingEdge(dut.clk)
        yield ReadOnly()
        print(dut.result)

    v = dut.result.value
    x, y, z = unpack_vector(v)
    x, y, z = (float_from_fixed(i) for i in (x, y, z))
    print(x, y, z)
    print(x ** 2 + y ** 2 + z ** 2)