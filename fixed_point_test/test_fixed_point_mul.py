from . import *
import cocotb
from cocotb.triggers import Timer

@cocotb.test()
def test_zero(dut):
    tb = FixedPointTestbench(dut)
    tb.set_inputs((0b101, 0b01), (0b11, 0b11))
    result = yield tb.get_result()
    yield tb.assert_result((15, 18), 0)
    print(result)
