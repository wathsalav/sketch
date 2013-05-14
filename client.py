#!/usr/bin/python

from entity import Entity
from eid import EID
from storage import Storage
from endpoint_session import Endpoint
from http_session import HTTPSession
import endpoint_session

import uuid
import hashlib
import base64
import json
import sys
import thread

def get_sha256_hash(idstr):
	key = "0123456789"
	shaObj = hashlib.sha256()
	shaObj.update(idstr+key)
	return (base64.b64encode(shaObj.digest()).decode()).encode()

def main():
#----------------------------Initialize your storage------------------------------------#
	if len(sys.argv) < 3:
		print "Expected: "+str(sys.argv[0])+" <config> <keyword> [output-file]"
	conf = __import__(str(sys.argv[1]), fromlist=["*"])
	"""Initialize storage plugin"""
	st = Storage(conf.store_plugin_mod, conf.store_plugin_class)
	st.connect(conf.store_ip, conf.store_port)
	
	#-------------------------------Find service/data endpoint----------------------------#
	"""Lookup documents by author <keyword>"""
	key = str(sys.argv[2])
	use_stdout = False
	if len(sys.argv) >= 4:
		out = str(sys.argv[3])
	else:
		out = sys.stdout
		use_stdout = True
	print "Looking up documents by "+key+"..."
	entity_json = st.get(key)
	entity_obj = json.loads(entity_json)
	ret_sid = entity_obj['sid']
	ret_name = entity_obj['name']
	print "Found document..."
	print "[Document Name]: "+ret_name
	print "[SID]: "+ret_sid
	"""Get EID of thsi SID"""
	eid_json = st.get(ret_sid.encode())
	eid = json.loads(eid_json)
	print "[EID]: "+eid['eid']
	"""Get EID - IP binding for this EID"""
	ip_addrs = st.get(eid['eid'].encode())
	print "[IP:PORT]: "+str(ip_addrs[0])+","+str(ip_addrs[1])
	
	print ret_name
	http_request = HTTPSession("GET", "/"+ret_name, eid['app_proto'])
	if use_stdout == True:
		xout = out
	else:
		xout = open(out, 'w')
	http_request.set_writer(xout)
	endpoint = Endpoint(st, eid_json)
	endpoint.add_app_proto_handler(http_request)
	endpoint_session.start_session()
	print "[DONE]"

if __name__ == '__main__':
	main()
