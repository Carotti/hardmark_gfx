from . import *
import logging
import cocotb
from cocotb.triggers import RisingEdge, ReadOnly, Timer
from cocotb.clock import Clock
from cocotb.result import ReturnValue, TestFailure
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
        
        self.log.info("Operand: {}".format(self.dut.op.value))
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

@cocotb.test()
def pipeline_test(dut):
    tb = NormalizeTestbench(dut)
    yield tb.initialize()

    yield tb.clock_input(make_fvec(-4.1, 3.1, -15))
    yield tb.clock_input(make_fvec(1, 2, 3))

    yield tb.flush_pipeline()

    yield tb.clock_assert_result(make_fvec(-0.25830078125, 0.1951904296875, -0.94482421875))
    yield tb.clock_assert_result(unpack_vector(40379922796153575315879L))

    yield tb.clock_input(make_fvec(3, 2, 1))

    yield tb.flush_pipeline()

    yield tb.clock_assert_result(make_fvec(0.8016357421875, 0.534423828125, 0.2672119140625))