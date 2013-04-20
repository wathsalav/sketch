import base_object

"""eid.py: Represents an Endpoint Identifier (EID) object"""
__author__	= "Wathsala Vithanage"
__email__	= "wathsala@princeton.edu"

class EID(base_object.BaseObject):
	"""Application level protocol"""
	app_proto = ""
	"""Transport level protocol"""
	trans_proto = ""
	"""Key of this EID"""
	eid = ""
	
	def __init__(self, eid, app_proto, trans_proto):
		self.eid = eid
		self.app_proto = app_proto
		self.trans_proto = trans_proto

	def get_key(self):
		return self.eid
		
