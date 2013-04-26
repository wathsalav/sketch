import base_object
import hashlib
import base64

"""entity.py: Entity represents an entity that we are interested in."""
__author__	= "Wathsala Vithanage"
__email__	= "wathsala@princeton.edu"


class Entity(base_object.BaseObject):
	"""Name of the entity"""
	name = ""

	"""Description of the service/data"""
	description = ""

	"""Content type of the service/data"""
	content_type = ""

	"""Content encoding of the service/data"""
	content_encoding = ""
	
	"""Entity type, data (D) or service (S)"""
	entity_type = ""

	"""SID of this entity"""
	sid = ""

	def __init__(self, name, description, content_type, content_encoding, entity_type):
		self.name = name
		self.description = description
		self.content_type = content_type
		self.content_encoding = content_encoding
		self.entity_type = entity_type
		self.sid = self.get_hash()


	def set_sid(self, sid):
		self.sid = sid

	def get_sid(self):
		return self.sid

