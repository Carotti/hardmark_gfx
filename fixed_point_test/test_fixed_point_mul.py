from . import *
import cocotb
from cocotb.triggers import Timer

@cocotb.test()
def test_zero_l_positive(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs((bitmask(integer_w - 1), bitmask(fraction_w)), (0, 0))
    yield tb.assert_result((0, 0), 0)

@cocotb.test()
def test_zero_l_negative(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs((bitmask(integer_w), bitmask(fraction_w)), (0, 0))
    yield tb.assert_result((0, 0), 0)

@cocotb.test()
def test_zero_r_positive(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs((0, 0), (bitmask(integer_w - 1), bitmask(fraction_w)))
    yield tb.assert_result((0, 0), 0)

@cocotb.test()
def test_zero_r_negative(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs((0, 0), (bitmask(integer_w), bitmask(fraction_w)))
    yield tb.assert_result((0, 0), 0)

@cocotb.test()
def signed_overflow(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs((1 << (integer_w - 1), 0), (1 << (integer_w - 1), 0))
    yield tb.assert_result((0, 0), 1)

@cocotb.test()
def signed_unsigned_overflow(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs((1 << (integer_w - 1), 0), (bitmask(integer_w - 1), bitmask(fraction_w)))
    yield tb.assert_result(unpack_if(1 << (integer_w - 1)), 1)

num_equivalence_tests = 100

@cocotb.test()
def test_multiplication_equivalence(dut):
    tb = FixedPointTestbench(dut)

    def overflow_calc(op1, op2):
        result = op1 * op2

        op1_sign = is_negative(op1)
        op2_sign = is_negative(op2)

        result = op1 * op2

        result_sign = ((result >> fixed_w) == bitmask(fixed_w))
        result_overflow = (not result_sign) & ((result >> fixed_w) != 0)
        result = (result >> fraction_w) & bitmask(fixed_w)

        if (((op1_sign != op2_sign) != result_sign) and result != 0) or result_overflow:
            overflow = 1
        else:
            overflow = 0

        return result, overflow

    yield tb.assert_equivalence_random(overflow_calc, num_equivalence_tests)