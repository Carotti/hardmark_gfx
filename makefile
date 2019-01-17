COCOTB = $(PWD)/cocotb
VERILOG_SOURCES = 	$(PWD)/fixed_point/fixed_point.sv \
					$(PWD)/fixed_point/fixed_point_sub.sv \
					$(PWD)/fixed_point/fixed_point_add.sv
MODULE = fixed_point_test
SIM_BUILD = sim_build/$(TOPLEVEL)
include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim