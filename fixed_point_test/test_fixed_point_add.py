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
    tb.set_inputs((bitmask(integer_w), 0), (1, 0))
    yield tb.assert_result((0, 0), 0)

@cocotb.test()
def test_overflow_unsigned(dut):
    tb = FloatingPointTestbench(dut)
    tb.set_inputs((bitmask(integer_w - 1), bitmask(fraction_w)), (0, 1))
    yield tb.assert_result((1 << (integer_w - 1), 0), 1)

@cocotb.test()
def test_fp_overflow(dut):
    tb = FloatingPointTestbench(dut)
    tb.set_inputs((0, bitmask(fraction_w)), (0, 1))
    yield tb.assert_result((1, 0), 0)

num_equivalence_tests = 100

@cocotb.test()
def test_addition_equivalence(dut):
    tb = FloatingPointTestbench(dut)

    def add(x, y):
        return x + y

    def overflow_calc(result, op1, op2):
        op1_sign = is_positive(op1)
        op2_sign = is_positive(op2)
        result_sign = is_positive(result)

        print(op1_sign)
        print(op2_sign)
        print(result_sign)
        print("RESULT" + bin(result))

        if (op1_sign == op2_sign and result_sign != op1_sign):
            return 1
        else:
            return 0

    yield tb.assert_equivalence_random(add, overflow_calc, num_equivalence_tests)
