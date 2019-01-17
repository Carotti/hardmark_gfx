COCOTB = $(PWD)/cocotb
VERILOG_SOURCES = 	$(PWD)/fixed_point/fixed_point.sv $(PWD)/fixed_point/fixed_point_add.sv
MODULE = fixed_point_test
include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim