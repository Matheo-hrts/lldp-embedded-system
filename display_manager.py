from PIL import Image, ImageDraw
from luma.core.reader import canvas

class DisplayManager:
    def __init__(self, device):
        self.device = device

    def show(self, draw_func):
        with canvas(self.device) as draw:
            draw_func(draw)

    def draw_func
