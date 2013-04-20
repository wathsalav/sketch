"""storage_api.py: Abstract storage plugins API"""
__author__	= "Wathsala Vithanage"
__email__	= "wathsala@pricneton.edu"

from abc import ABCMeta, abstractmethod

class StorageAPI(object):
	__metaclass__ = ABCMeta

	"""Setup the connection handle"""	
	@abstractmethod
	def connect(self, address, port):
		print "Setup the connection handle"

	"""Store a key, value pair"""
	@abstractmethod
	def put(self, key, value):
		print "Store a key, value pair"

	"""Get value by key"""
	@abstractmethod
	def get(self, key):
		print "Get value by key"

	"""Delete value by key"""
	@abstractmethod
	def delete(self, key):
		print "Delete value by key"
