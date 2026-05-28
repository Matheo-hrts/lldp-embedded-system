import gpiod
import time

BUTTONS = {
        73: "UP",
        70: "DOWN",
        75: "SELECT",
        72: "BACK",
        }

class InputManager:
    def __init__(self):
        self.chip = gpiod.Chip("/dev/gpiochip0")

        self.lines = self.chip.request_lines(
                consumer="buttons",
                config={
                    pin: gpiod.LineSettings(
                        direction=gpiod.line.Direction.INPUT
                        )
                    for pin in BUTTONS
                    }
                )
    def read_button(self):
        for pin, name in BUTTONS.items():
            value = self.lines.get_value(pin)

            if value == gpiod.line.Value.INACTIVE:
                time.sleep(0.25)
                return name

        return None
