from input_manager import InputManager
import time

inputs = InputManager()

while True:

    button = inputs.read_button()

    if button:
        print(button)

    time.sleep(0.05)
