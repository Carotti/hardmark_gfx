COCOTB = $(PWD)/cocotb
VERILOG_SOURCES = 	$(PWD)/fixed_point/* \
					$(PWD)/vector_math/* \
					$(PWD)/graphics/*
SIM_BUILD = sim_build/$(TOPLEVEL)
include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim