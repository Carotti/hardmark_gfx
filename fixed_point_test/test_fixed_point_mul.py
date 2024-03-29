from . import *
import cocotb
from cocotb.triggers import Timer
from testlib import *

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

@cocotb.test()
def two_by_two_negative(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs(unpack_if(fixed_from_float(-2)), unpack_if(fixed_from_float(-2)))
    yield tb.assert_result(unpack_if(fixed_from_float(4)), 0)

@cocotb.test()
def two_by_two(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs(unpack_if(fixed_from_float(2)), unpack_if(fixed_from_float(2)))
    yield tb.assert_result(unpack_if(fixed_from_float(4)), 0)

@cocotb.test()
def ten_by_ten_negative(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs(unpack_if(fixed_from_float(-10)), unpack_if(fixed_from_float(-10)))
    yield tb.assert_result(unpack_if(fixed_from_float(100)), 0)

@cocotb.test()
def ten_by_ten(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs(unpack_if(fixed_from_float(10)), unpack_if(fixed_from_float(10)))
    yield tb.assert_result(unpack_if(fixed_from_float(100)), 0)

@cocotb.test()
def found_vector_test1(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs(unpack_if(3760), unpack_if(16760832))
    yield tb.assert_result((2047,672), 0)

@cocotb.test()
def found_vector_test2(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs(unpack_if(fixed_from_float(0.05)), unpack_if(fixed_from_float(19.65576171875)))
    yield tb.assert_result(unpack_if(8039), 0)

@cocotb.test()
def line_test(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs(unpack_if(fixed_from_float(32.5625)), unpack_if(fixed_from_float(32.5625)))
    yield ReadOnly()
    print dut.result_sign
    print dut.op1_sign
    print dut.op2_sign
    print dut.result_overflow
    yield tb.assert_result((1060, 2592), 1)
    

num_equivalence_tests = 100

@cocotb.test()
def test_multiplication_equivalence(dut):
    tb = FixedPointTestbench(dut)

    yield tb.assert_equivalence_random(mul_operation, num_equivalence_tests)