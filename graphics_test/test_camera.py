import cocotb
from cocotb.triggers import ReadOnly, RisingEdge
from cocotb.clock import Clock
from testlib import *

@cocotb.test()
def test_camera(dut):
    cocotb.fork(Clock(dut.pixel_clk, 1, units="ns").start())

    for _ in range(31):
        yield RisingEdge(dut.pixel_clk)
        yield ReadOnly()
        print dut.ray