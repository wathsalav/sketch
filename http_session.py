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
	
	def __init__ (self, method, req_obj, version):
		self._method = method
		self._req_obj = req_obj
		self._version = version

	def _build_first_line(self):
		first_line = self._method+" "+self._req_obj+" "+self._version+"\r\n"
		return first_line
	
	def set_host(self, host):
		self._host = "Host: "+host+"\r\n"	

	
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
