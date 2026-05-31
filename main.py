from display_manager import DisplayManager
from input_manager import InputManager


def main():
    inputs = InputManager()
    manager = DisplayManager(inputs)
    manager.run()


if __name__ == "__main__":
    main()
