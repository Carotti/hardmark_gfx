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
    (
        make_fvec(-4.1, 3.1, -15),
        make_fvec(-0.25830078125, 0.1951904296875, -0.94482421875),
    ),
    (
        make_fvec(734, 12, -0.4),
        make_fvec(0.985595703125, 0.01611328125, -0.0006103515625),
    ),
    (
        make_fvec(-1342, 0.005, -12),
        make_fvec(-0.98291015625, 0.0, -0.0087890625),
    ),
    (
        make_fvec(-7, -3, -1.3),
        make_fvec(-0.90576171875, -0.38818359375, -0.168212890625),
    ),
    (
        make_fvec(0.05, 0.003, 0.009),
        make_fvec(0.9827880859375, 0.0576171875, 0.1754150390625),
    ),
    (
        make_fvec(0.33, 0.33, 0.33),
        make_fvec(0.5772705078125, 0.5772705078125, 0.5772705078125),
    ),
    (
        make_fvec(0.5772705078125, 0.5772705078125, 0.5772705078125),
        make_fvec(0.5772705078125, 0.5772705078125, 0.5772705078125),
    ),
]

@cocotb.coroutine
def run_test_single(dut, input_data):
    tb = NormalizeTestbench(dut)
    yield tb.initialize()

    op, result = input_data
    
    yield tb.clock_input(op)
    yield tb.flush_pipeline()
    yield tb.assert_result(result)
    
tests = TestFactory(run_test_single)
tests.add_option('input_data', inputs)
generate_tests_for(tests)

@cocotb.test()
def pipeline_test(dut):
    tb = NormalizeTestbench(dut)
    yield tb.initialize()

    for i in range(min(fixed_w, len(inputs))):
        op, _ = inputs[i]
        yield tb.clock_input(op)

    yield tb.flush_pipeline()

    for i in range(min(fixed_w, len(inputs))):
        _, result = inputs[i]
        yield tb.clock_assert_result(result)