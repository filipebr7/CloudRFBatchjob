#!/usr/bin/python
import csv, ssl, subprocess, os, urllib, urllib2, time, sys, random
# CloudRF API client script Copyright 2015 Farrant Consulting Ltd
#
# Reads in radio transmitter data from a CSV files and creates a propagation KMZ for each row
# Once complete, it will download the KMZ files
# The CSV file MUST be formatted according to the example!
# Before using you must create a CloudRF account and enter your API credentials in the data fields 'uid' and 'key'
# For help email: support@cloudrf.com

# CHANGE THESE SETTINGS
server="https://cloudrf.com" # Public server 
delay = 1 # Set to >8 for the public server or 0 if you own your own
googleearth=0 # Set to 0 to NOT open google earth after a successful calc
debug=0 # Set to 1 to see RAW parameters pre-send
domesh=1 # Set to 0 to only process sites. 1 to stitch together into a super layer 'mesh'
download=1 # Set to 0 to keep on the server, 1 to pull down an offline KMZ layer
# DO NOT EDIT BELOW HERE!

networks = []
uid = ""
nonce = random.randint(1,99)

o = urllib2.build_opener( urllib2.HTTPCookieProcessor()) 
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Send job to server. Refer to cloudrf.com/pages/api for API parameters.
def calculate(args):
	global uid
	nam = args.get('nam')
	net = args.get('net')+"_"+str(nonce) # Add nonce to avoid meshing unwanted legacy layers
	args['net']=net
	
	if net not in networks:
		networks.append(net)
		print "Adding network to list: "+net
		
	if args.get('uid') > 0:
		uid = args.get('uid')
	
	print "\nCalculating %s for %skm at %s pixels/degree..." % (nam,args.get('rad'),args.get('res'))
	
	# Build POST request
	data = urllib.urlencode(args)
	req = urllib2.Request(server+"/API/api.php", data)
	r = urllib2.urlopen(req, context=ctx)
	
	# Read in response.
	result = r.read()
	if download:
		downloadKMZ(result,nam)
		
	return result

# Download KMZ and launch in Google earth
def downloadKMZ(file,nam):
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
def mesh():
	global uid
	global networks
	# Omit '&kmz=1' to receive a EPSG 3857 PNG and lat/lon bounds
	#print networks
	
	for net in networks:
		meshurl=server+"/API/mesh/mesh.php?uid="+str(uid)+"&network="+net+"&kmz=1" # Knock off KMZ to receive web mercator bounds instead
		print "Creating mesh for network: "+net+"..."
		#print meshurl
		
		# Fetch URL with http GET
		req = urllib2.Request(meshurl)
		r = urllib2.urlopen(req, context=ctx)
		result = r.read()
		print result
		if download:
			downloadKMZ(result,net)

		
	
if len(sys.argv) == 1:
	print "ERROR: Need a .csv file\neg. python calculate.py mydata.csv"
	quit()
	
if not os.path.exists("kmz"):
		os.makedirs("kmz")
		
# Open CSV file
csvfile = csv.DictReader(open(sys.argv[1]))
n=0
for row in csvfile:
	# Pause script. Important otherwise server will refuse repeat requests
	time.sleep(delay)
	start_time = time.time() # Stopwatch start
	if debug:
		print row
	calculate(row)
	elapsed = round(time.time() - start_time,1) # Stopwatch stop
	print "Elapsed: "+str(elapsed)+"s"
	n=n+1
	

# Mesh now
if domesh:
	mesh()