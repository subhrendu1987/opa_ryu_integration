# ryu_opa_app.py
import json
import requests
from ryu.app import simple_switch_13
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4, tcp, udp

OPA_URL = "http://localhost:8181/v1/data"
headers = {"Content-Type": "application/json"}

class OPAIntegratingSwitch(simple_switch_13.SimpleSwitch13):
	OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

	def __init__(self, *args, **kwargs):
		super(OPAIntegratingSwitch, self).__init__(*args, **kwargs)

	@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
	def packet_in_handler(self, ev):
		msg = ev.msg
		ofproto = msg.datapath.ofproto
		pkt = packet.Packet(msg.data)
		#eth = pkt.get_protocol(ethernet.ethernet)
		tcp_pkt = pkt.get_protocol(tcp.tcp)
		udp_pkt = pkt.get_protocol(udp.udp)
		port = tcp_pkt.dst_port if tcp_pkt else (udp_pkt.dst_port if udp_pkt else None)
		print("L4-PORT:", port)
		if port:
			# Check with OPA
			dt=json.dumps({"input": {"port": port}})
			response = requests.post(OPA_URL, headers=headers, data=dt)
			print(response.text)
			parsed_data = json.loads(response.text)
			# Extract the 'allow' value
			decision = parsed_data["result"]["ryu_policy"]["allow"]
			#decision = response.json().get('allow', False)
		else:
			decision=True
		if decision:
			self.logger.info(f"Allowed port: {port}")
			super(OPAIntegratingSwitch, self)._packet_in_handler(ev)
			# Add flow or process packet as per SimpleSwitch13
		else:
			self.logger.info(f"Denied port: {port}")
			# Drop packet or take necessary action
