import cocotb
from cocotb.triggers import ReadOnly
from cocotb.result import TestFailure
from testlib import *

@cocotb.test()
def test_sub(dut):
    op1 = VectorSignal(dut.op1)
    op2 = VectorSignal(dut.op2)
    op1.assign(make_fvec(0, 0, 0))
    op2.assign(make_fvec(0, 10, 0))

    yield ReadOnly()

    if (unpack_vector(dut.result.value.integer) != (0, 4294885376, 0)):
        raise TestFailure()