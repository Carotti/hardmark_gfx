from . import *
import testlib
import cocotb
from cocotb.triggers import Timer, ReadOnly

@cocotb.test()
def test1(dut):
    op1 = VectorSignal(dut.op1)
    op2 = VectorSignal(dut.op2)

    op1.assign_xyz(fixed_from_float(1.0), fixed_from_float(2.0), fixed_from_float(3.0))
    op2.assign_xyz(fixed_from_float(3.0), fixed_from_float(2.0), fixed_from_float(1.0))

    yield ReadOnly()

    print(dut.result.value)