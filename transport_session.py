from http_session import HTTPSession
import base_object

"""transport_session.py: Transport Session"""
__author__	= "Wathsala Vithanage"
__email__	= "wathsala@princeton.edu"

class TCPSession(base_object.BaseObject):

	"""Application protocol handler associated with TCPSession\
	for instance HTTPSession."""	
	_app_proto_handler = ""
	
	def __init__(self, app_proto_handler):
		self._app_proto_handler = app_proto_handler

	def handle_protocol(self, p):
		p.sendMessage(self._app_proto_handler)
