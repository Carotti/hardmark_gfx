from . import *
import cocotb
from cocotb.triggers import Timer
from testlib import add_operation

@cocotb.test()
def test_zero(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs((0, 0), (0, 0))
    yield tb.assert_result((0, 0), 0)

@cocotb.test()
def test_overflow_signed(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs((bitmask(integer_w), 0), (1, 0))
    yield tb.assert_result((0, 0), 0)

@cocotb.test()
def test_overflow_unsigned(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs((bitmask(integer_w - 1), bitmask(fraction_w)), (0, 1))
    yield tb.assert_result((1 << (integer_w - 1), 0), 1)

@cocotb.test()
def test_fp_overflow(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs((0, bitmask(fraction_w)), (0, 1))
    yield tb.assert_result((1, 0), 0)

num_equivalence_tests = 100

@cocotb.test()
def test_addition_equivalence(dut):
    tb = FixedPointTestbench(dut)

    yield tb.assert_equivalence_random(add_operation, num_equivalence_tests)
