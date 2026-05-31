from unittest.mock import patch, MagicMock
from mail_manager import build_html, send_frame

SAMPLE_FRAME = {
    "system_name": "CiscoLLDP",
    "port_id": "Gi1/0/1",
    "ttl": "120"
}

def test_build_html_contains_values():
    html = build_html(SAMPLE_FRAME)

    assert "CiscoLLDP" in html
    assert "Gi1/0/1" in html
    assert "<table" in html

@patch("mail_manager.smtplib.SMTP")
def test_send_frame_sends_email(mock_smtp):
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    send_frame(SAMPLE_FRAME)

    mock_server.send_message.assert_called_once()
