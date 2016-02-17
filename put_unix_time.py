import time
import datetime
import json
import urllib2
from types import *
import requests

url = "http://swcon.asuscomm.com:64242/api/put"


def ostdb_restful_push():
	curtime = int(time.time())
	sname = "yung"
	data = {
		"metric": "syb.put_unixtime",
		"timestamp": time.time(),
		"value": curtime,
		"tags": {
			"sensor": "none",
			"name": sname,
			"floor_room": "6F_office",
			"building": "global_rnd_center",
			"owner": "yung",	
			"country": "kor"
		}
	}

	try: 
		ret = requests.post(url, data = json.dumps(data))
		print str(curtime)
		print ret
	except requests.exceptions.Timeout:
		logger.error("http connection error, Timeout %s",ret)
		print "Timeout Exception"
	except requests.exceptions.ConnectionError:
		logger.error("http connection error, Too many requests")
		print "Connection error"
		pass
	return 

if __name__ == "__main__":
	while (1):
		ostdb_restful_push()
		time.sleep(5)
