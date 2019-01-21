from . import *

import cocotb
from cocotb.triggers import RisingEdge, ReadOnly
from cocotb.clock import Clock
from testlib import *

@cocotb.test()
def normalize_test(dut):
    cocotb.fork(Clock(dut.clk, 1, units="ns").start())

    op = VectorSignal(dut.op)
    op.assign(make_fvec(1, 2, 3))

    yield ReadOnly()

    for _ in range(fixed_w):
        yield RisingEdge(dut.clk)
        yield ReadOnly()
        print(dut.result)