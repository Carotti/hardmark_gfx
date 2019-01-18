from . import *
import cocotb
from cocotb.triggers import Timer

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

    def add_operation(op1, op2):
        result = (op1 + op2) & bitmask(fixed_w)

        op1_sign = is_negative(op1)
        op2_sign = is_negative(op2)
        result_sign = is_negative(result)

        if (op1_sign == op2_sign and result_sign != op1_sign):
            overflow = 1
        else:
            overflow = 0

        return result, overflow

    yield tb.assert_equivalence_random(add_operation, num_equivalence_tests)
