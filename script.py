import requests
import subprocess
import time
import ottawaMaps


def retrieveParcel(minX, minY, filename, squareSize):
	r = requests.get("http://maps.ottawa.ca/ArcGIS/rest/services/Property_Parcels/MapServer/export?bbox=" + str(minX) + "%2C" + str(minY) + "%2C" + str(minX + squareSize) + "%2C" + str(minY + squareSize) + "&bboxSR=&layers=&layerdefs=&size=2048%2C2048&imageSR=&format=png32&transparent=true&dpi=200&time=&layerTimeOptions=&f=image", stream=True)
	if r.status_code == 200:
	    with open(filename, 'wb') as f:
			for chunk in r.iter_content(2048):
				f.write(chunk)

def retrievePhoto(minX, minY, filename, squareSize):
	r = requests.get("http://maps.ottawa.ca/ArcGIS/rest/services/Basemap_Imagery_2011/MapServer/export?bbox=" + str(minX) + "%2C" + str(minY) + "%2C" + str(minX + squareSize) + "%2C" + str(minY + squareSize) + "&bboxSR=&layers=&layerdefs=&size=2048%2C2048&imageSR=&format=png24&transparent=false&dpi=100000&time=&layerTimeOptions=&f=image", stream=True)
	if r.status_code == 200:
	    with open(filename, 'wb') as f:
			for chunk in r.iter_content(2048):
				f.write(chunk)

def mapFromBottomLeft(x, y, numHorizontal, numVertical, tileSize):
	rowNames = ""
	for row in range(0, numVertical):
		columnNames = ""
		for column in range(0, numHorizontal):
			tileName = str(row) + "-" + str(column) + ".png"
			retrievePhoto(x + column * tileSize, y + row * tileSize, tileName, tileSize)
			columnNames += tileName + " "

		subprocess.call("convert " + columnNames + "+append " + str(row) + ".png", shell=True)
		
		rowNames = str(row) + ".png" + " " + rowNames
		subprocess.call("rm " + columnNames, shell=True)

	resultName = str(numHorizontal) + "x" + str(numVertical) + "-result.png"
	subprocess.call("convert " + rowNames + "-append " + resultName, shell=True)
	subprocess.call("rm " + rowNames, shell=True)
	return resultName

def mapFromCenter(x, y, numHorizontal, numVertical, tileSize):
	xStart = x - ((numHorizontal * tileSize) / 2)
	yStart = y - ((numVertical * tileSize) / 2)
	return mapFromBottomLeft(xStart, yStart, numHorizontal, numVertical, tileSize)

def mapPropertyParcels(x, y, numHorizontal, numVertical, tileSize):
	x = x - ((numHorizontal * tileSize) / 2)
	y = y - ((numVertical * tileSize) / 2)
	rowNames = ""
	for row in range(0, numVertical):
		columnNames = ""
		for column in range(0, numHorizontal):
			tileName = str(row) + "-" + str(column) + ".png"
			retrieveParcel(x + column * tileSize, y + row * tileSize, tileName, tileSize)
			columnNames += tileName + " "

		subprocess.call("convert " + columnNames + "+append " + str(row) + ".png", shell=True)
		
		rowNames = str(row) + ".png" + " " + rowNames
		subprocess.call("rm " + columnNames, shell=True)

	resultName = str(numHorizontal) + "x" + str(numVertical) + "-parcels.png"
	subprocess.call("convert " + rowNames + "-append " + resultName, shell=True)
	subprocess.call("rm " + rowNames, shell=True)
	return resultName


print "Here are your options: "
counter = 0
d = ottawaMaps.getServices()
counter = 0
for option in d:
	print counter, option

# mapFromBottomLeft(-8445550.0, 5625162.0, 4, 5, 300)
mapName = mapFromCenter(-8444852.35, 5625877.5, 6, 6, 250)
parcelName = mapPropertyParcels(-8444852.35, 5625877.5, 6, 6, 250)

subprocess.call("convert " + mapName + " " + parcelName +  " -composite out.png", shell=True)
subprocess.call("rm " + mapName + " " + parcelName, shell=True)