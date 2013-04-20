"""memcache_plugin.py: A plugin class for memcache"""
__author__	= "Wathsala Vithanage"
__email__	= "wathsala@princeton.edu"

import storage_api
import memcache
 
class MemcachePlugin(storage_api.StorageAPI):
	
	"""The connection handle"""
	_handle = "" 
	
	def connect(self, address, port):
		connection_addr = address+":"+str(port)
		self._handle = memcache.Client([connection_addr], debug=1)	

	def put(self, key, value):
		self._handle.set(key, value)
	
	def get(self, key):
		return self._handle.get(key)

	def delete(self, key):
		self._handle.delete(key)
