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
from sys import stdout

def get_sha256_hash(idstr):
	key = "0123456789"
	shaObj = hashlib.sha256()
	shaObj.update(idstr+key)
	return (base64.b64encode(shaObj.digest()).decode()).encode()

#----------------------------Initialize your storage------------------------------------#
"""Initialize storage plugin"""
st = Storage('memcache_plugin', 'MemcachePlugin')
st.connect("127.0.0.1", 11211)


#------------------Create an endpoint, it's key and store it in the ring----------------#
"""Create a key for this endpoint"""
eid_uuid = "befe328c-676a-4f06-96fe-57df6b39140e"#uuid.uuid4()
xeid_key = get_sha256_hash(str(eid_uuid))
"""Create a service endpoint for this Data"""
xeid = EID(xeid_key, "HTTP/1.1", "TCP4")
"""Store this EID IP mapping in the ring"""
locations = []
locations.append('127.0.0.1:80')
locations.append('127.0.0.1:8080')
st.put(xeid_key, locations)

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

#---------------------------Store SID - EID mapping in the ring-----------------------#
"""Store this entity's EID under sid_str"""
st.put(sid_str, xeid.object2json())


#-------------------------------Find service/data endpoint----------------------------#
"""Lookup documents by author wathsala"""
print "Looking up documents by wathsala..."
entity_json = st.get('wathsala')
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

http_request = HTTPSession("GET", "/"+ret_name, eid['app_proto'])
#x1 = open('test1', 'w')
http_request.set_writer(stdout)
#http_request2 = HTTPSession("GET", "/sfasff", eid['app_proto'])
#http_request2.set_writer(stdout)
endpoint = Endpoint(st, eid_json)
endpoint.add_app_proto_handler(http_request)
#endpoint.add_app_proto_handler(http_request2)
endpoint_session.start_session()
print "[DONE]"
