from screens.home_screen import HomeScreen

def test_initial_selection():
    screen = HomeScreen()
    assert screen.selected == 0

def test_down_changes_selection():
    screen = HomeScreen()

    screen.handle_button("DOWN")

    assert screen.selected == 1

def test_up_wraps_selection():
    screen = HomeScreen()

    screen.handle_button("UP")

    assert screen.selected == 1

def test_select_returns_item():
    screen = HomeScreen()

    result = screen.handle_button("SELECT")

    assert result == "LLDP Data"
