import threading
from scapy.all import sniff
from scapy.contrib.lldp import *

def handle_packet(pkt, callback):
    chassis = pkt[LLDPDUChassisID].id
    port = pkt[LLDPDUPortID].id
    vlan = pkt[LLDPDUGenericOrganisationSpecific].subtype
    ttl = pkt[LLDPDUTimeToLive].ttl
    system = pkt[LLDPDUSystemName].system_name
    info = {
            "chassis_id" : chassis if isinstance(chassis, str) else chassis.decode(),
            "port_id" : port if isinstance(port, str) else port.decode(),
            "ttl" : ttl,
            "vlan" : vlan,
            "system_name" : system if isinstance(system, str) else system.decode(),
            }

    callback(info)

def start(iface, callback):
    def _sniff():
        sniff(iface=iface, prn=lambda pkt: handle_packet(pkt, callback), filter="ether proto 0x88cc")
    thread = threading.Thread(target=_sniff, daemon=True)
    thread.start()
