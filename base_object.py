import json

"""base_object.py: Base class of all the classes."""
__author__ 	= "Wathsla Vithanage"
__email__	= "wathsala@princeton.edu"

from abc import ABCMeta, abstractmethod

class BaseObject:
	def _to_builtin_type(self):
		d = {}
		d.update(self.__dict__)
		return d

	def object2json(self):
		return json.dumps(self, default=BaseObject._to_builtin_type)

	@abstractmethod
	def get_hash(self):
		return ""

