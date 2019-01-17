from . import *
import cocotb
from cocotb.triggers import Timer, ReadOnly
from cocotb.result import *

@cocotb.test()
def test_zero(dut):
    tb = FloatingPointTestbench(dut)
    tb.set_inputs((0, 0), (0, 0))
    yield tb.assert_result((0, 0), 0)

@cocotb.test()
def test_zero(dut):
    tb = FloatingPointTestbench(dut)
    tb.set_inputs((0, 0), (0, 0))
    yield tb.assert_result((0, 0), 0)