#!/usr/bin/python

from eid import EID
from storage import Storage
#from endpoint_cfg import *

import uuid
import hashlib
import base64
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
	
	"""Store this EID IP mapping in the ring"""
	xeid_key = get_sha256_hash(str(conf.eid_uuid))
	st.put(xeid_key, conf.locations)

if __name__ == '__main__':
	main()

