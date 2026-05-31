from unittest.mock import patch
from screens.history_screen import HistoryScreen

def test_refresh_loads_systems(monkeypatch):
    fake_history = [
        {
            "system_name": "Switch1",
            "timestamp": "2026"
        }
    ]

    monkeypatch.setattr(
        "screens.history_screen.load_history",
        lambda: fake_history
    )

    screen = HistoryScreen()

    assert screen.current_system == "Switch1"

@patch("screens.history_screen.send_frame")
def test_select_in_details_sends_email(mock_send):
    screen = HistoryScreen()

    screen._grouped_data = {
        "Switch1": [
            {"system_name": "Switch1", "timestamp": "2026"}
        ]
    }

    screen._systems = ["Switch1"]
    screen._state = "details"

    screen.handle_button("SELECT")

    mock_send.assert_called_once()
