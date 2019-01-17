from . import *
import cocotb
from cocotb.triggers import Timer

@cocotb.test()
def test_zero(dut):
    tb = FloatingPointTestbench(dut)
    tb.set_inputs((0, 0), (0, 0))
    yield tb.assert_result((0, 0), 0)

@cocotb.test()
def test_overflow_signed(dut):
    tb = FloatingPointTestbench(dut)
    tb.set_inputs((bitmask(integer_w), 0), (bitmask(integer_w), 0))
    yield tb.assert_result((0, 0), 0)

@cocotb.test()
def test_overflow_unsigned(dut):
    tb = FloatingPointTestbench(dut)
    tb.set_inputs((0, 0), (bitmask(integer_w - 1), bitmask(fraction_w)))
    yield tb.assert_result((1 << (integer_w - 1), 1), 0)

@cocotb.test()
def sub_to_zero(dut):
    tb = FloatingPointTestbench(dut)
    tb.set_inputs((bitmask(integer_w - 1), bitmask(fraction_w)), (bitmask(integer_w -1), bitmask(fraction_w)))
    yield tb.assert_result((0, 0), 0)

num_equivalence_tests = 100

@cocotb.test()
def test_addition_equivalence(dut):
    tb = FloatingPointTestbench(dut)

    def add(x, y):
        return x - y

    def overflow_calc(result, op1, op2):
        op1_sign = is_negative(op1)
        op2_sign = is_negative(op2)
        result_sign = is_negative(result)

        if (op1_sign != op2_sign and result_sign == op2_sign):
            return 1
        else:
            return 0

    yield tb.assert_equivalence_random(add, overflow_calc, num_equivalence_tests)
