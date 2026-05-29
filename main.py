import gpiod
from luma.core.render import canvas
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

def draw_loop(device, screen_holder):
    while True:
        img = Image.new("RGB", (320, 480), "white")
        draw = ImageDraw.Draw(img)
        screen_holder[0].draw(draw, 320, 480)
        img = img.rotate(90, expand=True)
        device.display(img)
        time.sleep(0.5)

def main():
    gpio = GpioWrapper()
    serial = spi(port=1, device=1, gpio_DC=79, gpio_RST=78, gpio=gpio)
    device = ili9488(serial, gpio=gpio, gpio_LIGHT=None)

    inputs = InputManager()

    home = HomeScreen()
    lldp = LLDPScreen()
    history = HistoryScreen()
    screen_holder = [home]

    draw_thread = threading.Thread(target=draw_loop, args=(device, screen_holder), daemon=True)
    draw_thread.start()


    while True:
        key = inputs.read_button()

        if not key:
            time.sleep(0.05)
            continue

        if key == "UP":
            device.clear()
            screen_holder[0].handle_button("UP")
        elif key == "DOWN":
            device.clear()
            screen_holder[0].handle_button("DOWN")
        elif key == "BACK":
            device.clear()
            result = screen_holder[0].handle_button("BACK")
            if result == "BACK":
                screen_holder[0] = home
        elif key == "SELECT":
            device.clear()
            result = screen_holder[0].handle_button("SELECT")
            if result == "LLDP Data":
                lldp.start_capture(iface="eth0")
                screen_holder[0]=lldp
            elif result == "SAVE":
                from storage_manager import save_csv
                save_csv(lldp._current_frame)
                print("Saved!")
            elif result == "History":
                history.refresh()
                screen_holder[0]=history
        elif key == "q":
            break

if __name__ == "__main__":
    main()
