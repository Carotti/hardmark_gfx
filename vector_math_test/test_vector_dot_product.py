from . import *
import testlib
import logging
import cocotb
from cocotb.triggers import Timer, ReadOnly
from cocotb.result import ReturnValue, TestFailure
from cocotb.regression import TestFactory

class DotProductTestbench:
    def __init__(self, dut):
        self.dut = dut
        self.op1 = VectorSignal(dut.op1)
        self.op2 = VectorSignal(dut.op2)

        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

    def set_inputs(self, op1, op2):
        self.op1.assign(op1)
        self.op2.assign(op2)

    @cocotb.coroutine
    def get_result(self):
        yield ReadOnly()
        raise ReturnValue(self.dut.result.value.integer)

    @cocotb.coroutine
    def assert_result(self, result, overflow):
        result_actual = yield self.get_result()
        overflow_actual = self.dut.overflow
        
        self.log.info("Operand1: {}".format(self.dut.op1.value))
        self.log.info("Operand2: {}".format(self.dut.op2.value))
        self.log.info("Result:   {}".format(self.dut.result.value))

        if (result != result_actual):
            raise TestFailure("Result incorrect: Got {} Expected {}".format(result_actual, result))

        if (overflow != overflow_actual):
            raise TestFailure("Overflow incorrect: Got {} Expected {}".format(overflow_actual, overflow))

def positive_overflow(index):
    op1 = [0 for _ in VEC_DIRS]
    op2 = [0 for _ in VEC_DIRS]
    op1[index] = bitmask(fixed_w - 1)
    op2[index] = bitmask(fixed_w - 1)
    value = ( # Positive overflow in index
        tuple(op1),
        tuple(op2),
        (bitmask(fraction_w) << integer_w),
        1,
    )
    return value

def total_overflow_positive(index):
    op1 = [fixed_from_float(1) for _ in VEC_DIRS]
    op2 = [1 for _ in VEC_DIRS]
    op2[index] = bitmask(fixed_w - 1)
    value = ( # Positive overflow on total sum only
        tuple(op1), 
        tuple(op2),
        (((1 << (fixed_w - 1)) + 1) & bitmask(fixed_w)),
        1,
    )
    return value

# Inputs created for integer_w: 19, fraction_w 13
# probably still work for other widths
inputs = [
    ( # Simple integer test
        make_fvec(3, 2, 1), 
        make_fvec(1, 2, 3),
        fixed_from_float(10),
        0,
    ),
    ( # Simple fractional test
        make_fvec(0.5, 2, 1), 
        make_fvec(1, 2, 3),
        fixed_from_float(7.5),
        0,
    ),
    ( # Simple negative test, positive result
        make_fvec(0.5, 2, -1), 
        make_fvec(1, 2, 3),
        fixed_from_float(1.5),
        0,
    ),
    ( # Simple negative test, negative result
        make_fvec(0.5, 2, -1), 
        make_fvec(1, -2, 3),
        fixed_from_float(-6.5),
        0,
    ),
] \
    + [positive_overflow(i) for i in VEC_DIRS] \
    + [total_overflow_positive(i) for i in VEC_DIRS]

@cocotb.coroutine
def run_test(dut, input_data):
    tb = DotProductTestbench(dut)

    op1, op2, result, overflow = input_data
    tb.set_inputs(op1, op2)

    yield tb.assert_result(result, overflow)
    
tests = TestFactory(run_test)
tests.add_option('input_data', inputs)
generate_tests_for(tests)