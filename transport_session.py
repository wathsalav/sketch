from http_session import HTTPSession
import Queue

import base_object

"""transport_session.py: Transport Session"""
__author__	= "Wathsala Vithanage"
__email__	= "wathsala@princeton.edu"

class TCPSession(base_object.BaseObject):

	"""Application protocol handlers associated with TCPSession\
	for instance HTTPSession."""	
	_app_proto_queue = ""

	"""IP address of this TCP connection"""
	_ip_addr = ""

	"""Remote port of this TCP connection"""
	_port = ""

	#"""Twisted endpoint protocol"""
	#_endpoint_proto = ""
	

	def __init__(self, ip_addr, port):
		self._app_proto_queue = Queue.Queue()
		self._ip_addr = ip_addr
		self._port = port

	def handle_protocol(self, endpoint_protocol):
		#endpoint_protocol.setQueue(self._app_proto_queue)
		x = True
		while x == True:
			ap = self._app_proto_queue.get(True, 1)
			endpoint_protocol.sendMessage(ap)

	def add_app_proto_handler(self, app_proto_handler):
		app_proto_handler.set_host(self._ip_addr)
		app_proto_handler.set_port(self._port)
		self._app_proto_queue.put_nowait(app_proto_handler)

