import base_object

"""transport_session.py: Transport Session"""
__author__	= "Wathsala Vithanage"
__email__	= "wathsala@princeton.edu"

class TCPSession(base_object.BaseObject):
	_app_proto = ""

	def __init__(self, app_proto):
		self._app_proto = app_proto

	def handle_protocol(self, p):
		print "Hello...", self._app_proto
		p.sendMessage("Hello")
		reactor.callLater(1, p.sendMessage, "This is sent in a second")
		reactor.callLater(2, p.transport.closeConnection())
