from PIL import ImageFont
from network_manager import start
import threading

class LLDPScreen:
    def __init__(self):
        self._current_frame = None
        self._timed_out = False
        self._timeout_timer = None

    def start_capture(self, iface="eth0"):
        start(iface=iface, callback=self.on_frame_received)
        self._timeout_timer = threading.Timer(40, self.on_timeout)
        self._timeout_timer.start()

    def on_frame_received(self, info: dict):
        if self._timeout_timer:
            self._timeout_timer.cancel()
        self._timed_out = False
        self._current_frame = info
        self._timeout_timer = threading.Timer(40, self.on_timeout)
        self._timout_timer.start()

    def on_timeout(self):
        self._timed_out = True
        self._current_frame = None

    def draw(self, draw, width, height):
        draw.rectangle((0, 0, width, height), fill="black")
        draw.text((10, 10), "LLDP Data", fill="white")
        draw.line([(0,30), (width, 30)], fill="white")

        if self._timed_out:
            draw.text((10, 50), "No frame received!", fill="red")
        elif self._current_frame is None:
            draw.text((10, 50), "waiting for data...", fill="yellow")
        else:
            y=50
            for key, value in self._current_frame.items():
                draw.text((10, y), f"{key}: {value}", fill="white")
                y += 25

    def handle_button(self, button):
        if button == "BACK":
            if self._timeout_timer:
                self._timeout_timer.cancel()
            return "BACK"
        elif button == "SELECT" and self._current_frame:
            return "SAVE"
