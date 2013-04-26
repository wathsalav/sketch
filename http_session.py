from http_parser.parser import HttpParser

import base_object

"""http_session.py: Represents an HTTP Session"""
__author__	= "Wathsala Vithanage"
__email__	= "wathsala@princeton.edu"

class HTTPSession(base_object.BaseObject):

	_http_header = ""
	_method = ""
	_version = ""
	_req_obj = ""
	_user_agent = "User-Agent: COS-598C-Project-Client\r\n"
	_accept = "Accept: */*\r\n"
	_accept_enc = "Accept-Encoding: *\r\n"
	_accept_charset = "Accept-Charset: *\r\n"
	_host = ""
	_writer = ""
	_closeable = False
	_http_parser = ""
	_nr_bytes = 0
	
	def __init__ (self, method, req_obj, version):
		self._method = method
		self._req_obj = req_obj
		self._version = version
		self._http_parser = HttpParser()

	def _build_first_line(self):
		first_line = self._method+" "+self._req_obj+" "+self._version+"\r\n"
		return first_line
	
	def set_host(self, host):
		self._host = "Host: "+host+"\r\n"	

	def set_writer(self, writer):
		self._writer = writer

	def write_response(self, data):
		recved = len(data)
		nparsed = self._http_parser.execute(data, recved)
		assert nparsed == recved
		self._nr_bytes += recved	
		if self._http_parser.is_partial_body():
			self._writer.write(str(self._http_parser.recv_body()))

		if self._http_parser.is_message_complete():
			self._closeable = True
		return self._nr_bytes
		
	def get_response_headers(self):
		if self._http_parser.is_headers_complete():
                	return self._http_parser.get_headers()

	def closeable(self):
		return self._closeable

	def set_port(self, port):
		return

	def get_request(self):
		self._http_header = self._build_first_line()+\
					self._host+\
					self._user_agent+\
					self._accept+\
					self._accept_enc+\
					self._accept_charset+\
					"\r\n"
		return self._http_header
