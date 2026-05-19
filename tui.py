from textual.app import App

from screens.home_screen import HomeScreen

class LLDPApp(App):
    def on_mount(self) -> None:
        self.push_screen(HomeScreen())
