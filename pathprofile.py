#!/usr/bin/python
import csv, ssl, subprocess, os, urllib, urllib2, time, sys, random
# CloudRF API client script Copyright 2016 Farrant Consulting Ltd
#
# Reads in radio transmitter data from a CSV files and creates a propagation KMZ for each row
# Once complete, it will download the KMZ files
# The CSV file MUST be formatted according to the example!
# Before using you must create a CloudRF account and enter your API credentials in the data fields 'uid' and 'key'
# For help email: support@cloudrf.com

# CHANGE THESE SETTINGS
server="https://cloudrf.com" # Public server 
debug=0 # Set to 1 to see RAW parameters pre-send
download=1 # Set to 0 to keep on the server, 1 to pull down an offline KMZ layer
# DO NOT EDIT BELOW HERE!

networks = []
uid = ""
nonce = random.randint(1,99)

o = urllib2.build_opener( urllib2.HTTPCookieProcessor()) 
try:
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE
except:
	pass

# Send job to server. Refer to cloudrf.com/pages/api for API parameters.
def calculate(args,nam):
	global uid
	if args.get('uid') > 0:
		uid = args.get('uid')
	print "Calculating path from %s,%s to %s,%s..." % (args.get('tla'),args.get('tlo'),args.get('rla'),args.get('rlo'))
	
	# Build POST request
	data = urllib.urlencode(args)
	req = urllib2.Request(server+"/API/ppa/ppa.php", data)
	try:
		r = urllib2.urlopen(req, context=ctx)
	except:
		r = urllib2.urlopen(req)

	# Read in response.
	result = r.read()
	if download:
		downloadPPA(server+result+".txt",nam+".txt") # TEXT REPORT
		downloadPPA(server+result+".png",nam+".png") # PNG IMAGE
		print "Downloaded as ppa/"+nam
	else:
		print result

# Download KMZ and launch in Google earth
def downloadPPA(file,nam):
	f = o.open(file)
	localFile=os.path.join("ppa",nam)
	response = ""
	while 1:
		data = f.read()
		if not data:
			break
		response += data

	with open(localFile, "wb") as local_file:
		local_file.write(response)

	
	
if len(sys.argv) == 1:
	print "ERROR: Need a .csv file\neg. python calculate.py mydata.csv"
	quit()
	
if not os.path.exists("ppa"):
		os.makedirs("ppa")
		
# Open CSV file
csvfile = csv.DictReader(open(sys.argv[1]))
n=1
for row in csvfile:
	start_time = time.time() # Stopwatch start
	if debug:
		print row
	calculate(row,str(n))
	elapsed = round(time.time() - start_time,1) # Stopwatch stop
	n=n+1
	
