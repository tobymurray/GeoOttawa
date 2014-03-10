import requests
import re

def getServices():
	apiList =[]
	namesList = []
	r = requests.get("http://maps.ottawa.ca/ArcGIS/rest/services")
	for line in r.text.split('\n'):
		if (line.encode('ascii','ignore').startswith("<li><a href=\"/ArcGIS/rest/services/")):
			for xml in line.split('"'):
				token = xml.encode('ascii','ignore').strip()
				if len(token) > 0 and '<' not in token and '>' not in token :
					apiList.append(token)
			for xml in re.split("<.*?>", line):
				token = xml.encode('ascii','ignore').strip()
				if len(token) > 0 and token != "(MapServer)" and token != "(GeometryServer)"  and token != "(GeocodeServer)" :
					namesList.append(token)
	return dict(zip(namesList, apiList))