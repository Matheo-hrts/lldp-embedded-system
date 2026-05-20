from screens.lldp_data_screen import LLDPDataScreen
from screens.history_screen import HistoryScreen

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button
from textual.containers import Vertical

class HomeScreen(Screen):
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Button("LLDP Data", id="lldp_data")
            yield Button("History", id="history")
            yield Button("Mail", id="mail")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "lldp_data":
            self.app.push_screen(LLDPDataScreen())

        if event.button.id == "history":
            self.app.push_screen(HistoryScreen())
