"""memcache_plugin.py: A plugin class for memcache"""
__author__	= "Wathsala Vithanage"
__email__	= "wathsala@princeton.edu"

import storage_api

class Storage(storage_api.StorageAPI):
	
	_st_plugin = {}

	def __init__(self, mod_name, class_name):
		mod = __import__(mod_name)
		klass = getattr(mod, class_name)
		self._st_plugin = klass()

	def connect(self, address, port):
		self._st_plugin.connect(address, port)
	
	def put(self, key, value):
		self._st_plugin.put(key, value)
	
	def get(self, key):
		return self._st_plugin.get(key)

	def delete(self, key):
		self._st_plugin.delete(key)

