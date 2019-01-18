from . import *
import cocotb
from cocotb.triggers import Timer

@cocotb.test()
def test_zero_l(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs((513, 13), (0, 0))
    yield tb.assert_result((0, 0), 0)

@cocotb.test()
def test_zero_r(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs((0, 0), (513, 13))
    yield tb.assert_result((0, 0), 0)

@cocotb.test()
def signed_overflow(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs((1 << (integer_w - 1), 0), (1 << (integer_w - 1), 0))
    yield tb.assert_result((0, 0), 1)

num_equivalence_tests = 100

@cocotb.test()
def test_multiplication_equivalence(dut):
    tb = FixedPointTestbench(dut)

    def overflow_calc(op1, op2):
        result = op1 * op2

        op1_sign = is_negative(op1)
        op2_sign = is_negative(op2)

        result = op1 * op2

        result_sign = ((result >> fixed_w) != 0)
        result = (result >> fraction_w) & bitmask(fixed_w)

        if (op1_sign != op2_sign) != result_sign:
            overflow = 1
        else:
            overflow = 0

        return result, overflow

    yield tb.assert_equivalence_random(overflow_calc, num_equivalence_tests)