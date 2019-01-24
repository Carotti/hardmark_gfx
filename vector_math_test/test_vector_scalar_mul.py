from . import *
import testlib
import logging
import cocotb
from cocotb.triggers import Timer, ReadOnly
from cocotb.result import ReturnValue, TestFailure
from cocotb.regression import TestFactory

class ScalarMulTestbench:
    def __init__(self, dut):
        self.dut = dut
        self.vector_op = VectorSignal(dut.vector_op)

        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

    def set_inputs(self, op1, op2):
        self.vector_op.assign(op2)
        self.dut.scalar_op.value = op1

    @cocotb.coroutine
    def get_result(self):
        yield ReadOnly()
        result = self.dut.result.value.integer
        raise ReturnValue(unpack_vector(result))

    @cocotb.coroutine
    def assert_result(self, result, overflow):
        result_actual = yield self.get_result()
        overflow_actual = self.dut.overflow
        
        self.log.info("Operand1: {}".format(self.dut.scalar_op.value))
        self.log.info("Operand2: {}".format(self.dut.vector_op.value))
        self.log.info("Result:   {}".format(self.dut.result.value))

        if (result != result_actual):
            raise TestFailure("Result incorrect: Got {} Expected {}".format(result_actual, result))

        if (overflow != overflow_actual):
            raise TestFailure("Overflow incorrect: Got {} Expected {}".format(overflow_actual, overflow))

def positive_overflow(index):
    scalar_amt = 1.25
    scalar_op = fixed_from_float(scalar_amt)
    vector_op = [0 for _ in VEC_DIRS]
    result = [0 for _ in VEC_DIRS]

    vector_op[index] = bitmask(fixed_w - 1)
    result[index] = fixed_from_float(float_from_fixed(vector_op[index]) * scalar_amt)

    value = (
        scalar_op,
        tuple(vector_op),
        tuple(result),
        1,
    )
    return value

# Inputs created for integer_w: 19, fraction_w 13
# probably still work for other widths
inputs = [
    ( # Zero vector * 0
        0,
        make_fvec(0, 0, 0),
        make_fvec(0, 0, 0),
        0,
    ),
    ( # Non-zero vector * 0
        0,
        make_fvec(1, 2, 3),
        make_fvec(0, 0, 0),
        0,
    ),
    ( # Vector of 1s
        fixed_from_float(3.125),
        make_fvec(1, 1, 1),
        make_fvec(3.125, 3.125, 3.125),
        0,
    ),
    ( # Scalar 1
        fixed_from_float(1),
        make_fvec(1.25, 3.125, 0),
        make_fvec(1.25, 3.125, 0),
        0,
    ),
    ( # 32
        fixed_from_float(16),
        make_fvec(-1.96484375, 2.03515625, 2.0),
        make_fvec(-31.4375, 32.5625, 32.0),
        0,
    ),
]

@cocotb.coroutine
def run_test(dut, input_data):
    tb = ScalarMulTestbench(dut)

    op1, op2, result, overflow = input_data
    tb.set_inputs(op1, op2)

    yield tb.assert_result(result, overflow)
    
tests = TestFactory(run_test)
tests.add_option('input_data', inputs)
generate_tests_for(tests)