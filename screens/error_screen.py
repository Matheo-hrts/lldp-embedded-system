from PIL import ImageFont

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)

class ErrorScreen:
    def __init__(self):
        self.error = ""

    def set_error(self, message):
        self.eror = str(message)

    def draw(self, draw, width, height):
        draw.rectangle((0, 0, width, height), fill="black")

        draw.text((10, 10), "ERROR", fill="red", font=font)

        draw.line([(0,30), (width, 30)], fill="white")

        if self.error:
            draw.text((10, 50), self.error[:120], fill="black", font=font)

    def handle_button(self, button):
        if button == "BACK":
            return "BACK"

        return None
        
