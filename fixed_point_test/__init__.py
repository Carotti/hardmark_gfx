import cocotb
from cocotb.result import *
from cocotb.triggers import ReadOnly, Timer
import os
import random
import logging

TOPLEVEL = os.getenv("TOPLEVEL")

dir_path = os.path.dirname(os.path.realpath(__file__))

test_file = dir_path + "/test_" + TOPLEVEL + ".py"

print(test_file)
execfile(test_file)

integer_w = 19
fraction_w = 13

def bitmask(width):
    return (1 << width) - 1

def unpack_if(n):
    return (n >> fraction_w) & bitmask(integer_w), n & bitmask(fraction_w)

def pack_if(if_value):
    i, f = if_value
    return ((i << fraction_w) & (bitmask(integer_w) << fraction_w)) | (f & bitmask(fraction_w))

def dup(x):
    return x, x

def is_negative(n):
    return (n & (1 << (integer_w + fraction_w - 1))) != 0

def fixed_from_float(n):
    return (int)(n * (1 << fraction_w))

def float_from_fixed(n):
    return (float)(n) / (float)(1 << fraction_w)


class FixedPointTestbench:
    def __init__(self, dut):
        self.dut = dut

        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

    def set_inputs(self, op1, op2):
        op1_value = pack_if(op1)
        op2_value = pack_if(op2)

        self.dut.op1.value = op1_value
        self.dut.op2.value = op2_value

    @cocotb.coroutine
    def get_result(self):
        yield ReadOnly()

        ir, fr = unpack_if(self.dut.result.value)

        overflow = self.dut.overflow.value

        raise ReturnValue((ir, fr, overflow))

    @cocotb.coroutine
    def assert_result(self, result, overflow):
        integer, fraction = result
        integer_actual, fraction_actual, overflow_actual = yield self.get_result()

        self.log.info("Operand1: {}".format(self.dut.op1.value))
        self.log.info("Operand2: {}".format(self.dut.op2.value))
        self.log.info("Result:   {}".format(self.dut.result.value))

        if (integer != integer_actual):
            raise TestFailure("Integer incorrect: Got {} Expected {}".format(integer_actual, integer))

        if (fraction != fraction_actual):
            raise TestFailure("Fraction incorrect: Got {} Expected {}".format(fraction_actual, fraction))

        if (overflow != overflow_actual):
            raise TestFailure("Overflow incorrect: Got {} Expected {}".format(overflow_actual, overflow))

    @cocotb.coroutine
    def assert_equivalence(self, operands, op, overflow_calc):
        op1, op2 = operands
        self.set_inputs(unpack_if(op1), unpack_if(op2))
        result = op(op1, op2) & bitmask(integer_w + fraction_w)
        overflow = overflow_calc(result, op1, op2)
        yield self.assert_result(unpack_if(result), overflow)

    @cocotb.coroutine
    def assert_equivalence_random(self, op, overflow_calc, num):

        for _ in range(num):
            operands = dup(random.randint(0, 2 ** (integer_w + fraction_w - 1)))
            yield self.assert_equivalence(operands, op, overflow_calc)
            yield Timer(1)