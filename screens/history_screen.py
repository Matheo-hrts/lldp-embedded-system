from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Label, Button
from textual.containers import Vertical, ScrollableContainer, Horizontal

from storage_manager import load_history
from storage_manager import group_by_system

class HistoryScreen(Screen):

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("No history yet!", id="empty")
        with Horizontal():
            with ScrollableContainer(id="names_column"):
                pass
            with ScrollableContainer(id="dates_column"):
                pass
            with ScrollableContainer(id="details_column"):
                pass
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#names_column").display = False
        read_data = load_history()
        grouped_data = group_by_system(read_data)
        if grouped_data:
            self.on_history_read(grouped_data)


    def on_history_read(self, data: list) -> None:
        self._grouped_data = data
        self.query_one("#empty").display = False
        names = self.query_one("#names_column")
        names.display = True
        dates = self.query_one("#dates_column")
        dates.display = True
        details = self.query_one("#details_column")
        details.display = True
        names.remove_children()
        for system_name in data.keys():
            names.mount(Button(system_name, id=f"name_{system_name}"))
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id.startswith("name_"):
            system_name = event.button.id.removeprefix("name_")
            self._selected_system = system_name
            frames = self._grouped_data[self._selected_system]
            dates_column = self.query_one("#dates_column")
            dates_column.display = True
            dates_column.remove_children()
            for dates_data, frame in enumerate(frames):
                dates_column.mount(Button(frame["timestamp"], id=f"date_{dates_data}"))

        elif event.button.id.startswith("date_"):
            dates_data = int(event.button.id.removeprefix("date_"))
            frame = self._grouped_data[self._selected_system][dates_data]
            details_column = self.query_one("#details_column")
            details_column.display = True
            details_column.remove_children()
            for key, value in frame.items():
                details_column.mount(Label(f"{key}: {value}"))
