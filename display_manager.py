import gpiod
from luma.core.interface.serial import spi
from luma.lcd.device import ili9488
from screens.home_screen import HomeScreen
from screens.lldp_screen import LLDPScreen
from screens.history_screen import HistoryScreen
import time
import threading
from PIL import Image, ImageDraw
from input_manager import InputManager


class GpioWrapper:
    OUT = 1
    IN = 0
    LOW = 0
    HIGH = 1

    def __init__(self):
        self.chip = gpiod.Chip("/dev/gpiochip0")
        self.lines = {}

    def setmode(self, mode):
        pass

    def setup(self, pin, direction):
        if pin is None:
            return
        line = self.chip.request_lines(
            consumer="luma",
            config={pin: gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT)}
        )
        self.lines[pin] = line

    def output(self, pin, value):
        if pin is None:
            return
        self.lines[pin].set_value(pin, gpiod.line.Value.ACTIVE if value else gpiod.line.Value.INACTIVE)

    def cleanup(self):
        for line in self.lines.values():
            line.release()


class DisplayManager:
    def __init__(self):
        self.gpio = GpioWrapper()
        serial = spi(port=1, device=1, gpio_DC=79, gpio_RST=78, gpio=self.gpio)
        self.device = ili9488(serial, gpio=self.gpio, gpio_LIGHT=None)
        self.inputs = InputManager()

        self.home = HomeScreen()
        self.lldp = LLDPScreen()
        self.history = HistoryScreen()
        self.screen_holder = [self.home]

    def _draw_loop(self):
        while True:
            img = Image.new("RGB", (320, 480), "white")
            draw = ImageDraw.Draw(img)
            self.screen_holder[0].draw(draw, 320, 480)
            img = img.rotate(90, expand=True)
            self.device.display(img)
            time.sleep(0.5)

    def run(self):
        draw_thread = threading.Thread(target=self._draw_loop, daemon=True)
        draw_thread.start()

        while True:
            key = self.inputs.read_button()
            if not key:
                time.sleep(0.05)
                continue

            if key == "UP":
                self.device.clear()
                self.screen_holder[0].handle_button("UP")

            elif key == "DOWN":
                self.device.clear()
                self.screen_holder[0].handle_button("DOWN")

            elif key == "BACK":
                self.device.clear()
                result = self.screen_holder[0].handle_button("BACK")
                if result == "BACK":
                    self.screen_holder[0] = self.home

            elif key == "SELECT":
                self.device.clear()
                result = self.screen_holder[0].handle_button("SELECT")
                if result == "LLDP Data":
                    self.lldp.start_capture(iface="eth0")
                    self.screen_holder[0] = self.lldp
                elif result == "SAVE":
                    from storage_manager import save_csv
                    save_csv(self.lldp._current_frame)
                    self.screen_holder[0] = self.home
                elif result == "History":
                    self.history.refresh()
                    self.screen_holder[0] = self.history

            elif key == "q":
                break
