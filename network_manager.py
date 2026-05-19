import threading
from scapy.all import sniff
from scapy.contrib.lldp import *

def handle_packet(pkt, callback):
    info = {
            "chassis_id" : pkt[LLDPDUChassisID].id,
            "port_id" : pkt[LLDPDUPortID].id.decode(),
            "ttl" : pkt[LLDPDUTimeToLive].ttl,
            "system_name" : pkt[LLDPDUSystemName].system_name.decode(),
            }

    callback(info)

def start(iface, callback):
    def _sniff():
        sniff(iface=iface, prn=lambda pkt: handle_packet(pkt, callback), filter="ether proto 0x88cc")
    thread = threading.Thread(target=_sniff, daemon=True)
    thread.start()
