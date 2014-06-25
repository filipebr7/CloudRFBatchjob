#!/usr/bin/python
import csv, subprocess, os, urllib, urllib2, time, sys
# CloudRF API client script Copyright 2014 Farrant Consulting Ltd
#
# Reads in radio transmitter data from a CSV files and creates a propagation KMZ for each row
# Once complete, it will download the KMZ files
# The CSV file MUST be formatted according to the example!
# Before using you must create a CloudRF account and enter your API credentials in the data fields 'uid' and 'key'
# For help email: support@cloudrf.com

# CHANGE THESE SETTINGS
server="https://web.cloudrf.com" # Public server 
delay = 4 # Set to >8 for the public server or 0 if you own your own
googleearth=0 # Set to 0 to NOT open google earth after a successful calc
debug=0 # Set to 1 to see RAW parameters pre-send
domesh=1 # Set to 0 to only process sites. 1 to stitch together into super layer
# DO NOT EDIT BELOW HERE!

calcs = []
uid = ""

o = urllib2.build_opener( urllib2.HTTPCookieProcessor()) 

# Send job to server. Refer to cloudrf.com/pages/api for API parameters.
def calculate(args):
	global uid
	nam = args.get('nam')
	if args.get('uid') > 0:
		uid = args.get('uid')
	
	print "\nCalculating %s for %skm at %s pixels/degree..." % (nam,args.get('rad'),args.get('res'))
	
	# Build POST request
	data = urllib.urlencode(args)
	req = urllib2.Request(server+"/API/api.php", data)
	r = urllib2.urlopen(req)
	
	# Read in response. Hopefully a file http://...
	result = r.read()
	if "http" in result:
		print result
		calcs.append(result.replace(server+"/users/"+uid+"/",""))
		
		# Success! Download KMZ
		download(result,nam)
	else:
		print result

# Download KMZ and launch in Google earth
def download(file,nam):
	f = o.open(file)
	localFile="kmz\\"+nam+".kmz"
	response = ""
	while 1:
		data = f.read()
		if not data:
			break
		response += data

	with open(localFile, "wb") as local_file:
		local_file.write(response)
	print "Downloaded as "+localFile
	if googleearth:
		# Launch Google earth (if installed and associated with .kmz)
		os.startfile(localFile) 
	
#Stitch calcs into super layer (mesh)	
def mesh(calcs):
	global uid
	# Omit '&kmz=1' to receive a EPSG 3857 PNG and lat/lon bounds
	meshurl=server+"/API/mesh/mesh.php?uid="+str(uid)+"&name=mesh&kmz=1&calcs="
	print "\nStitching mesh..."
	for layer in calcs:
		meshurl=meshurl+layer.replace(".kmz\n","")+","
	
	# Fetch URL with http GET
	req = urllib2.Request(meshurl)
	r = urllib2.urlopen(req)
	result = r.read()
	if "http" in result:
		print result
		download(result,"mesh")
	else:
		print result
	
	
if len(sys.argv) == 1:
	print "ERROR: Need a .csv file\neg. python calculate.py mydata.csv"
	quit()
	
if not os.path.exists("kmz"):
		os.makedirs("kmz")
		
# Open CSV file
csvfile = csv.DictReader(open(sys.argv[1]))
for row in csvfile:
	# Pause script. Important otherwise server will refuse repeat requests
	time.sleep(delay)
	start_time = time.time() # Stopwatch start
	if debug:
		print row
	calculate(row)
	elapsed = round(time.time() - start_time,1) # Stopwatch stop
	print "Elapsed: "+str(elapsed)+"s"
	

# Mesh now
mesh(calcs)