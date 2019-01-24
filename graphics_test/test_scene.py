import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ReadOnly, RisingEdge, Timer
from cocotb.result import ReturnValue

from PIL import Image

class SceneTestbench:

    @staticmethod
    def get_total_size(width, fp, sync, bp):
        return sum(i.value.integer for i in (width, fp, sync, bp))

    def __init__(self, dut):
        self.dut = dut

        cam = dut.main_camera
        self.width = cam.hWidth.value.integer
        self.height = cam.vWidth.value.integer
        self.total_width = SceneTestbench.get_total_size(cam.hWidth, cam.hFrontPorch, cam.hSyncWidth, cam.hBackPorch)
        self.total_height = SceneTestbench.get_total_size(cam.vWidth, cam.vFrontPorch, cam.vSyncWidth, cam.vBackPorch)

        self.pipeline_latency = fixed_w - 1

    @cocotb.coroutine
    def initialize(self):
        cocotb.fork(Clock(self.dut.pixel_clk, 1, units="ns").start())
        yield Timer(0)

    @cocotb.coroutine
    def flush_pipeline(self):
        for _ in range(self.pipeline_latency):
            yield RisingEdge(self.dut.pixel_clk)

    @cocotb.coroutine
    def get_image(self):
        yield self.flush_pipeline()

        image = Image.new("RGBA", (self.width, self.height))

        for y in range(10):
            for x in range(self.total_width):
                yield RisingEdge(self.dut.pixel_clk)
                if x < self.width and y < self.height:
                    yield ReadOnly()
                    pixel = self.dut.pixel_data.value.integer
                    print x, y
                    print self.dut.pixel_data

                    if ((x == 311 or x == 312 or x == 313) and y == 4):
                        print self.dut.main_camera.unnormalized_ray

                    if (x == 336 and y == 4):
                        raise TestSuccess()
                    
                    r = (pixel >> 24) & bitmask(8)
                    g = (pixel >> 16) & bitmask(8)
                    b = (pixel >> 8) & bitmask(8)
                    a = pixel & bitmask(8)
                    image.putpixel((x, y), (r, g, b, a))

        image.save("tmp.png")

@cocotb.test()
def scene_test(dut):
    tb = SceneTestbench(dut)
    yield tb.initialize()

    yield tb.get_image()