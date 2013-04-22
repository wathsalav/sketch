import json
import re
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint
from sys import stdout

import base_object
import storage
from transport_session import TCPSession

"""endpoint_seesion.py: Representation of a session with an endpoint.
   Session is always associated with an endpoint represented by an EID"""
__author__	= "Wathsala Vithanage"
__email__	= "wathsala@princetone.edu"


class Endpoint(base_object.BaseObject):
	
	_eidObject = ""
	_eidJSON = ""
	_endpoint = ""
	_store = ""
	_ipaddrs = ""
	_currentAddr = 0
	_splitter = ""
	_client_endpoint = ""
	_trasnport_session = ""

	def __init__(self, store, eidJSON):
		self._eidJSON = eidJSON
		self._eidObject = json.loads(self._eidJSON)
		self._store = store
		self._ipaddrs = self._store.get((self._eidObject['eid']).encode())
		self._splitter = re.compile(r'([:])')
		ipp_pair = self._splitter.split(self._ipaddrs[self._currentAddr])
		if self._eidObject['trans_proto'] == 'TCP4':
			self._init_TCP4(ipp_pair[0], int(ipp_pair[2]), self._eidObject['app_proto'])
		reactor.run()
	
	def _init_TCP4(self, ip, port, app_proto):
		self._endpoint = TCP4ClientEndpoint(reactor, ip, port)
		self._client_endpoint = self._endpoint.connect(EndpointFactory())
		self._transport_session = TCPSession(app_proto)
		self._client_endpoint.addCallback(self._transport_session.handle_protocol)


class EndpointProtocol(Protocol):
	def dataReceived(self, data):
		stdout.write(data)


class EndpointFactory(ClientFactory):
	def startedConnecting(self, connector):
		print 'Started to connect.'

	def buildProtocol(self, addr):
		print 'Connected.'
		return EndpointProtocol()

	def clientConnectionLost(self, connector, reason):
		print 'Lost connection.  Reason:', reason

	def clientConnectionFailed(self, connector, reason):
		print 'Connection failed. Reason:', reason

