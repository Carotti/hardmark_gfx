import os

from testlib import *

# This has to be done in the top level testing module
def generate_tests_for(factory):
    factory.generate_tests()

TOPLEVEL = os.getenv("TOPLEVEL")
dir_path = os.path.dirname(os.path.realpath(__file__))
test_file = dir_path + "/test_" + TOPLEVEL + ".py"
execfile(test_file)