from . import *
import logging
import cocotb
from cocotb.triggers import RisingEdge, ReadOnly, Timer
from cocotb.clock import Clock
from cocotb.result import ReturnValue, TestFailure
from cocotb.regression import TestFactory
from testlib import *

class NormalizeTestbench:
    def __init__(self, dut):
        self.dut = dut
        self.op = VectorSignal(dut.op)

        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.pipeline_latency = fixed_w

    @cocotb.coroutine
    def initialize(self):
        cocotb.fork(Clock(self.dut.clk, 1, units="ns").start())
        yield Timer(0)

    def set_inputs(self, op):
        self.op.assign(op)

    @cocotb.coroutine
    def clock_input(self, op):
        if self.pipeline_latency <= 0:
            raise ValueError("Can't clock in any more inputs with this pipeline depth")

        self.set_inputs(op)
        yield RisingEdge(self.dut.clk)
        self.pipeline_latency -= 1

    @cocotb.coroutine
    def get_result(self):
        yield ReadOnly()

        result = self.dut.result.value.integer
        raise ReturnValue(unpack_vector(result))

    @cocotb.coroutine
    def assert_result(self, result):
        result_actual = yield self.get_result()
        
        self.log.info("Result:  {}".format(self.dut.result.value))

        if (result != result_actual):
            raise TestFailure("Result incorrect: Got {} Expected {}".format(result_actual, result))

    @cocotb.coroutine
    def clock_assert_result(self, result):
        if self.pipeline_latency > fixed_w:
            raise ValueError("This output is undefined for this pipeline depth")

        yield self.assert_result(result)
        yield RisingEdge(self.dut.clk)
        self.pipeline_latency += 1

    @cocotb.coroutine
    def flush_pipeline(self):
        for _ in range(self.pipeline_latency):
            yield RisingEdge(self.dut.clk)

inputs = [
    make_fvec(1, 1, 1),
    make_fvec(-4.1, 3.1, -15),
    make_fvec(734, 12, -0.4),
    make_fvec(-1342, 0.005, -12),
    make_fvec(-7, -3, -1.3),
    make_fvec(0.05, 0.003, 0.009),
    make_fvec(0.33, 0.33, 0.33),
    make_fvec(0.5772705078125, 0.5772705078125, 0.5772705078125),
    make_fvec(-1.96484375, 2.03515625, 2.0),
]

@cocotb.coroutine
def run_test_single(dut, input_data):
    tb = NormalizeTestbench(dut)
    yield tb.initialize()

    op = input_data
    x, y, z = op
    result = normalize_vector_operation(pack_vector(x, y, z))
    
    yield tb.clock_input(op)
    yield tb.flush_pipeline()
    yield tb.assert_result(unpack_vector(result))
    
tests = TestFactory(run_test_single)
tests.add_option('input_data', inputs)
generate_tests_for(tests)

@cocotb.test()
def pipeline_test(dut):
    tb = NormalizeTestbench(dut)
    yield tb.initialize()

    for i in range(min(fixed_w, len(inputs))):
        yield tb.clock_input(inputs[i])

    yield tb.flush_pipeline()

    for i in range(min(fixed_w, len(inputs))):
        x, y, z = inputs[i]
        result = normalize_vector_operation(pack_vector(x, y, z))
        yield tb.clock_assert_result(unpack_vector(result))