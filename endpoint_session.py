import json
import re

from twisted.internet import epollreactor
epollreactor.install()
from twisted.internet import reactor

from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint
from sys import stdout
from threading import Thread, Lock
import Queue

import base_object
import storage
from transport_session import TCPSession

from twisted.internet.defer import setDebugging
setDebugging(True)
from sys import stdout
from twisted.python import log
log.startLogging(stdout)

"""endpoint_seesion.py: Representation of a session with an endpoint.
   Session is always associated with an endpoint represented by an EID"""
__author__	= "Wathsala Vithanage"
__email__	= "wathsala@princetone.edu"

def start_session():
	reactor.run()

def stop_session():
	reactor.stop()

class Endpoint(base_object.BaseObject):

	"""EID object for this endpoint"""	
	_eid_object = ""
	"""JSON representation of EID object for this endpoint"""
	_eid_json = ""
	"""Endpoint object of Twister"""
	_endpoint = ""
	"""Storage of the system"""
	_store = ""
	"""IP Addresses this endpoint is associated with"""
	_ipaddrs = ""
	"""Current IP,PORT pair in use. Used when\
	 re-establishing connection with endpoint."""
	_current_addr = 0
	"""This is the splitter used to separate ports from IP addresses."""
	_splitter = ""
	"""Endpoint created by Twister for the client"""
	_client_endpoint = ""
	"""This is the trasnport session object, TCPSession or UDPSession"""
	_trasnport_session = ""

	def __init__(self, store, eid_json):
		self._eid_json = eid_json
		self._eid_object = json.loads(self._eid_json)
		self._store = store
		self._ipaddrs = self._store.get((self._eid_object['eid']).encode())
		self._splitter = re.compile(r'([:])')
		ipp_pair = self._splitter.split(self._ipaddrs[self._current_addr])
		self._transport_session = TCPSession(ipp_pair[0], int(ipp_pair[2]))
		if self._eid_object['trans_proto'] == 'TCP4':
			self._init_TCP4(ipp_pair[0], int(ipp_pair[2]))
		
	
	def _init_TCP4(self, ip, port):
		self._endpoint = TCP4ClientEndpoint(reactor, ip, port)
		self._client_endpoint = self._endpoint.connect(EndpointFactory())
		#reactor.callLater(10, self._reinit_TCP4)
		self._client_endpoint.addCallback(self._transport_session.handle_protocol)
		self._client_endpoint.addErrback(self._errback)

	def _errback(self, failure):
		self._current_addr = self._current_addr + 1
		try: 
			ipp_pair = self._splitter.split(self._ipaddrs[self._current_addr])
			if self._eid_object['trans_proto'] == 'TCP4':
				self._init_TCP4(ipp_pair[0], int(ipp_pair[2]))
		except IndexError:
			print "No more endpoints to try!"
			stop_session()

	def add_app_proto_handler(self, app_proto_handler):
		self._transport_session.add_app_proto_handler(app_proto_handler) 



class EndpointProtocol(Protocol):

	"""Application protocol handler associated with TCPSession\
	for instance HTTPSession."""	
	_app_proto_handler = None
	
	_queue = Queue.Queue()

	def dataReceived(self, data):
		if self._app_proto_handler is None:
			self._app_proto_handler = self._queue.get()
		self._app_proto_handler.write_response(data)
		if self._app_proto_handler.closeable():
			self._app_proto_handler = None
			

	def sendMessage(self, app_proto_handler):
		print app_proto_handler.get_request()
		wb = self.transport.write(str(app_proto_handler.get_request()))
		self._queue.put_nowait(app_proto_handler)


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

