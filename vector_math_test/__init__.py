import os

from testlib import *

# This has to be done in the top level testing module
def generate_tests_for(factory):
    factory.generate_tests()

TOPLEVEL = os.getenv("TOPLEVEL")
dir_path = os.path.dirname(os.path.realpath(__file__))
test_file = dir_path + "/test_" + TOPLEVEL + ".py"
execfile(test_file)

class VectorSignal:
    def __init__(self, handle):
        self.handle = handle

    def assign_xyz(self, x, y, z):
        self.handle.value = pack_vector(x, y, z)

    def assign(self, v):
        x, y, z = v
        self.assign_xyz(x, y , z)