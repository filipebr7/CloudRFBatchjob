#!/usr/bin/python
import requests, csv, subprocess, os, urllib2, time, sys
# CloudRF API client script Copyright 2014 Farrant Consulting Ltd
#
# Reads in radio transmitter data from data.csv and creates a propagation KMZ for each row
# Once complete, it will download the KMZ and launch it with Google earth
# The CSV file MUST be formatted according to the example!
# Before using you must create a CloudRF account and enter your UID and password in the relevant fields below
# support@cloudrf.com

apiurl="https://m.cloudrf.com/API/api.php" # Public server 
delay = 1 # Set to >8 for the public server or 0 if you own your own
# DO NOT EDIT BELOW HERE

o = urllib2.build_opener( urllib2.HTTPCookieProcessor()) 

# Send job to server. Refer to cloudrf.com/docs/api for API parameters.
def calculate(args):
	nam = args.get('nam')
	print "Calculating %s for %skm at %s pixels/degree..." % (nam,args.get('rad'),args.get('res'))
	r = requests.post(apiurl, data=args)
	if "http" in r.text:
		download(r.text,nam)
	else:
		print r.text

# Download KMZ and launch in Google earth
def download(file,nam):
	f = o.open(file)
	localFile=nam+".kmz"
	response = ""
	while 1:
		data = f.read()
		if not data:
			break
		response += data

	with open(localFile, "wb") as local_file:
		local_file.write(response)
	print "Downloaded as "+localFile
	os.startfile(localFile) # Launch Google earth (if installed)
	
	
if len(sys.argv) == 1:
	print "ERROR: Need a .csv file\neg. python calculate.py mydata.csv"
	quit()
	
# Open CSV file
csvfile = csv.DictReader(open(sys.argv[1]))
for row in csvfile:
	start_time = time.time() # Stopwatch start
	calculate(row)
	elapsed = round(time.time() - start_time,1) # Stopwatch stop
	print "Elapsed time: "+str(elapsed)+"s"
	time.sleep(delay)
