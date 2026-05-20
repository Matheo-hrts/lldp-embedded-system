from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Label
from textual.containers import Vertical

from network_manager import start
from storage_manager import save_csv

class LLDPDataScreen(Screen):

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Waiting for LLDP data...", id="waiting")
        with Vertical(id="data_container"):
            pass
        yield Label("No LLDP data received!", id="timeout")
        yield Button("Save", id="save")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#timeout").display = False
        self.query_one("#save").display = False

        start(iface="end0", callback=lambda info: self.app.call_from_thread(self.on_frame_received, info))

        self.timeout_timer = self.set_timer(40, self.on_timeout)

    def on_frame_received(self, info: dict) -> None:
        self.timeout_timer.stop()
        self.timeout_timer = self.set_timer(40, self.on_timeout)

        self._current_frame = info

        self.query_one("#waiting").display = False
        self.query_one("#timeout").display = False
        self.query_one("#save").display = True

        container = self.query_one("#data_container")
        container.display = True
        container.remove_children()
        for key, value in info.items():
            container.mount(Label(f"{key}: {value}"))
        

    def on_timeout(self) -> None:
        self.query_one("#waiting").display = False
        self.query_one("#data_container").display = False
        self.query_one("#save").display = False
        self.query_one("#timeout").display = True 

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save" and hasattr(self, "_current_frame"):
            save_csv(self._current_frame)
