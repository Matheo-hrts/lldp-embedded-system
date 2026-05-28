from PIL import ImageFont

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)

class HomeScreen:
    def __init__(self):
        self.items = ["LLDP Data", "History"]
        self.selected = 0

    def draw(self, draw, width, height):
        draw.rectangle((0, 0, width, height), fill="black")
        draw.text((10, 10), "LLDP Monitor", fill="white", font=font)
        draw.line([(0,30), (width, 30)], fill="white")
        for i, item in enumerate(self.items):
            y = 50 + i * 40

            draw.rectangle((0, y-5, width, y+25), fill="black")
            if i == self.selected:
                draw.rectangle((0, y-5, width, y+25), fill="white")
                draw.text((20, y), item, fill="black", font=font)
            else:
                draw.text((20, y), item, fill="white", font=font)

    def handle_button(self, button):
        if button == "UP":
            self.selected = (self.selected - 1) % len(self.items)
        elif button == "DOWN":
            self.selected = (self.selected + 1) % len(self.items)
        elif button == "SELECT":
            return self.items[self.selected]
        elif button == "BACK":
            return None
