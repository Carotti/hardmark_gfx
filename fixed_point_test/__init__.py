import cocotb
from cocotb.result import *
from cocotb.triggers import ReadOnly
import os

TOPLEVEL = os.getenv("TOPLEVEL")

dir_path = os.path.dirname(os.path.realpath(__file__))

execfile(dir_path + "/test_" + TOPLEVEL + ".py")

integer_w = 19
fraction_w = 13

def bitmask(width):
    return (1 << width) - 1

class FloatingPointTestbench:
    def __init__(self, dut):
        self.dut = dut

    def set_inputs(self, op1, op2):
        i1, f1 = op1
        i2, f2 = op2

        op1_value = (i1 << fraction_w) & (bitmask(integer_w) << fraction_w)
        op1_value |= f1 & bitmask(fraction_w)

        op2_value = (i2 << fraction_w) & (bitmask(integer_w) << fraction_w)
        op2_value |= f2 & bitmask(fraction_w)

        self.dut.op1.value = op1_value
        self.dut.op2.value = op2_value

    @cocotb.coroutine
    def get_result(self):
        yield ReadOnly()

        result_value = self.dut.result.value

        ir = (result_value >> fraction_w)
        fr = result_value & bitmask(fraction_w)

        overflow = self.dut.overflow

        raise ReturnValue((ir, fr, overflow))

    @cocotb.coroutine
    def assert_result(self, result, overflow):
        integer, fraction = result
        integer_actual, fraction_actual, overflow_actual = yield self.get_result()

        if (integer != integer_actual):
            raise TestFailure("Integer incorrect")

        if (fraction != fraction_actual):
            raise TestFailure("Fraction incorrect")

        if (overflow != overflow_actual):
            raise TestFailure("Overflow incorrect")