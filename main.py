import entity
import eid
import storage

import uuid
import hashlib
import base64
import json

def get_sha256_hash(idstr):
	key = "0123456789"
	shaObj = hashlib.sha256()
	shaObj.update(idstr+key)
	return (base64.b64encode(shaObj.digest()).decode()).encode()

#----------------------------Initialize your storage------------------------------------#
"""Initialize storage plugin"""
st = storage.Storage('memcache_plugin', 'MemcachePlugin')
st.connect("127.0.0.1", 11211)


#------------------Create an endpoint, it's key and store it in the ring----------------#
"""Create a key for this endpoint"""
eid_uuid = uuid.uuid4()
xeid_key = get_sha256_hash(str(eid_uuid))
"""Create a service endpoint for this Data"""
xeid = eid.EID(xeid_key, "HTTP/1.1", "TCP")
"""Store this EID IP mapping in the ring"""
locations = []
locations.append('127.0.0.1:80')
locations.append('127.0.0.1:8080')
st.put(xeid_key, locations)

#-----------------------Create an entity and store it in registry----------------------#
"""Create an entity"""
xentity = entity.Entity("A bogus document inserted to demonstrate the software", "Wathsala Object", "text/xml", "xyz", "D")
"""Create an SID string for the entity"""
uuid = uuid.uuid4()
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
ret_eid = json.loads(eid_json)['eid']
print "[EID]: "+ret_eid
"""Get EID - IP binding for this EID"""
ip_addrs = st.get(ret_eid.encode())
print "[IP:PORT]: "+str(ip_addrs[0])+","+str(ip_addrs[1])
