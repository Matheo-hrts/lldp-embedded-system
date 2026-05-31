from unittest.mock import MagicMock
from network_manager import handle_packet

def test_handle_packet_extracts_info():
    pkt = MagicMock()

    pkt.__getitem__.side_effect = lambda x: {
        "LLDPDUChassisID": MagicMock(id="aa:bb:cc"),
        "LLDPDUPortID": MagicMock(id=b"Gi1/0/1"),
        "LLDPDUTimeToLive": MagicMock(ttl=120),
        "LLDPDUSystemName": MagicMock(system_name=b"Switch1"),
    }[x.__name__]

    result = {}

    def callback(info):
        result.update(info)

    handle_packet(pkt, callback)

    assert result["system_name"] == "Switch1"
