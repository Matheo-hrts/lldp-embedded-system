from PIL import ImageFont
from mail_manager import get_recipients

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)

class MailListScreen:
    def __init__(self):
        self.recipients = []
        self.selected_index = 0

    def refresh(self):
        self.recipients = get_recipients()
        self.selected_index = 0

    @property
    def selected_mail(self):
        if self.recipients:
            return self.recipients[self.selected_index]
        return None

    def draw(self, draw, width, height):
        draw.rectangle((0,0, width, height), fill="black")
        draw.text((10,10), "Send To:", fill="white", font=font)
        draw.line([(0,30), (width, 30)], fill="white")
        
        if not self.recipients:
            draw.text((10,50), "No recipients configured", fill="red", font=font)
            return

        y = 50
        for i, address in enumerate(self.recipients):
            if i == self.selected_index:
                draw.rectangle((0,y-5,width, y+20), fill="white")
                draw.text((10,y), address, fill="black", font=font)
            else: 
                draw.text((10,y), address, fill="white", font=font)
            y += 25

        draw.text((10, height -25), "SELECT: choose BACK: cancel", fill="white", font=font)
    def handle_button(self, button):
        if not self.recipients:
            return "BACK" if button == "BACK" else None

        if button == "UP":
            self.selected_index = (self.selected_index - 1) % len(self.recipients)
        elif button == "DOWN":
            self.selected_index = (self.selected_index + 1) % len(self.recipients)
        elif button == "BACK":
            return "BACK"
        elif button == "SELECT":
            return "SEND_EMAIL"
        return None
