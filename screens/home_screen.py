from PIL import ImageFont

class HomeScreen:
    def __init__(self):
        self.items = ["LLDP Data", "History", "Mail"]
        self.selected = 0

    def draw(self, draw, width, height):
        draw.rectangle((0, 0, width, height), fill="black")
        draw.text((10, 10), "LLDP Monitor", fill="white")
        draw.line([(0,30), (width, 30)], fill="white")
        for i, item in enumerate(self.items):
            y = 50 + i * 40

            draw.rectangle((0, y-5, width, y+25), fill="black")
            if i == self.selected:
                draw.rectangle((0, y-5, width, y+25), fill="white")
                draw.text((20, y), item, fill="black")
            else:
                draw.text((20, y), item, fill="white")

    def handle_button(self, button):
        if button == "UP":
            self.selected = (self.selected - 1) % len(self.items)
        elif button == "DOWN":
            self.selected = (self.selected + 1) % len(self.items)
        elif button == "SELECT":
            return self.items[self.selected]
        elif button == "BACK":
            return None
