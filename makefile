COCOTB = $(PWD)/cocotb
VERILOG_SOURCES = 	$(PWD)/fixed_point/fixed_point.sv \
					$(PWD)/fixed_point/fixed_point_sub.sv \
					$(PWD)/fixed_point/fixed_point_add.sv \
					$(PWD)/fixed_point/fixed_point_mul.sv
SIM_BUILD = sim_build/$(TOPLEVEL)
include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim