#!/usr/bin/python

from entity import Entity
from eid import EID
from storage import Storage

import uuid
import hashlib
import base64
import json
import sys

def get_sha256_hash(idstr):
	key = "0123456789"
	shaObj = hashlib.sha256()
	shaObj.update(idstr+key)
	return (base64.b64encode(shaObj.digest()).decode()).encode()



def main():
#----------------------------Initialize your storage------------------------------------#
	if len(sys.argv) < 2:
		print "Expected: "+str(sys.argv[0])+" <config>"
	conf = __import__(str(sys.argv[1]), fromlist=["*"])
	"""Initialize storage plugin"""
	st = Storage(conf.store_plugin_mod, conf.store_plugin_class)
	st.connect(conf.store_ip, conf.store_port)

	"""Create a service endpoint for up coming Data"""
	xeid_key = get_sha256_hash(str(conf.eid_uuid))
	xeid = EID(xeid_key, conf.app_proto, conf.transport)
	
	#-----------------------Create an entity and store it in registry----------------------#
	"""Create an entity"""
	xentity = Entity("WathsalaObject", "A bogus document inserted to demonstrate the software", "text/xml", "xyz", "D")
	"""Create an SID string for the entity"""
	uuid = "50aec6e5-1968-4243-a51c-ab1768a2c514"#uuid.uuid4()
	sid_str = get_sha256_hash(str(uuid))
	xentity.set_sid(sid_str)
	xjson = xentity.object2json()
	"""Store this entity in author registry"""
	st.put("wathsala", xjson)
	
	"""Store this entity's EID under sid_str"""
	st.put(sid_str, xeid.object2json())
	
if __name__ == '__main__':
	main()

