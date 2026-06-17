from PIL import ImageFont
from storage_manager import load_history
from storage_manager import group_by_system
from mail_manager import send_frame

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)

class HistoryScreen:
    def __init__(self):
        self._state = "systems"
        self._saved_data = load_history()
        self._grouped_data = group_by_system(self._saved_data)
        self._systems = list(self._grouped_data.keys())
        self._selected_system_index = 0
        self._selected_frame_index = 0
        self._frame_to_send = None

    @property
    def current_system(self):
        if not self._systems:
            return None
        return self._systems[self._selected_system_index]

    @property
    def current_frames(self):
        if not self.current_system:
            return []
        return self._grouped_data[self.current_system]

    def draw(self, draw, width, height):
        draw.rectangle((0, 0, width, height), fill="black")
        draw.text((10, 10), "History", fill="white", font=font)
        draw.line([(0,30), (width, 30)], fill="white")

        if not self._systems:
            draw.text((5, 30), "No history", fill="red", font=font)
            return

        if self._state == "systems":
            y = 50

            for i, system in enumerate(self._systems):
                if i == self._selected_system_index:
                    draw.rectangle((0, y-5, width, y+20), fill ="white")
                    draw.text((10,y), system, fill="black", font=font)
                else:
                    draw.text((10, y), system, fill="white", font=font)
                y += 20

        elif self._state == "dates":
            frames = self.current_frames
            y = 50

            for i, frame in enumerate(frames):
                if i == self._selected_frame_index:
                    draw.rectangle((0, y-5, width, y+20), fill ="white")
                    draw.text((10,y), frame["timestamp"][:19], fill="black", font=font)
                else:
                    draw.text((10, y), frame["timestamp"][:19], fill="white", font=font)
                y += 20

        elif self._state == "details":
            frame = self.current_frames[self._selected_frame_index]
            y = 50

            for key, value in frame.items():
                if y > width - 50:
                    break
                draw.text((5, y), f"{key}: {value}", fill="white", font=font)
                y += 18

            draw.rectangle((5, width-130, width-5, width-100), fill="white")
            draw.text((10, width-120), "SELECT: Send via Email", fill="black", font=font)

    def refresh(self):
        self._saved_data = load_history()
        self._grouped_data = group_by_system(self._saved_data)
        self._systems = list(self._grouped_data.keys())
        self._selected_system_index = 0
        self._selected_frame_index = 0
        self._state = "systems"

    def send_to(self, address):
        send_frame(self._frame_to_send, address)
    
    def handle_button(self, button):
        if self._state == "systems":
            if button == "BACK":
                return "BACK"

            if button == "DOWN":
                self._selected_system_index = min(
                        self._selected_system_index + 1,
                        len(self._systems) - 1
                        )
            elif button == "UP":
                self._selected_system_index = max(
                        self._selected_system_index - 1,
                        0
                        )

            elif button == "SELECT":
                self._state = "dates"

        elif self._state == "dates":
            frames = self.current_frames

            if button == "DOWN":
                self._selected_frame_index = min(
                        self._selected_frame_index + 1,
                        len(frames) - 1
                        )

            elif button == "UP":
                self._selected_frame_index = max(
                        self._selected_frame_index - 1,
                        0
                        )

            elif button == "SELECT":
                self._state = "details"

            elif button == "BACK":
                self._state = "systems"
        
        elif self._state == "details":

            if button == "SELECT":
                self._frame_to_send = self.current_frames[self._selected_frame_index]
                return "EMAIL_LIST"

            if button == "BACK":
                self._state = "dates"

        return None
        
