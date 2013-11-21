#!/usr/bin/python
import requests, csv, subprocess, os, urllib2, time

# CloudRF API client script Copyright 2013 Farrant Consulting Ltd
# Permission is given to do what you want with this.
#
# Reads in radio transmitter data from data.csv and creates a propagation KMZ for each row
# Once complete, it will download the KMZ and launch it with Google earth
# The CSV file MUST be formatted according to the example.
# Before using you must create a CloudRF account and enter your UID and key in the relevant fields below
# support@cloudrf.com

o = urllib2.build_opener( urllib2.HTTPCookieProcessor() 

# Change before using. You will need to update the apiurl if you have purchased your own server
uid="0" # CLOUDRF USER ID
key="YOURAPIKEYHERE" # SHA1 HASH OF YOUR CLOUDRF PASSWORD
apiurl="https://m.cloudrf.com/API/api.php"

# Send job to server> Refer to cloudrf.com for API parameters.
def calculate(ant,azi,clh,cli,col,dbm,dis,erp,fbr,fmt,frq,gry,hbw,key,lat,lon,nam,opy,out,pol,rad,res,rxh,ter,tlt,txh,uid,vbw):
	args = {'ant': ant, 'azi': azi, 'clh': clh, 'cli': cli,'col': col,'dbm':dbm,
	'dis':dis,'erp':erp,'fbr':fbr,'fmt':fmt,'frq':frq,'gry':gry,'hbw':hbw,'key':key,
	'lat':lat,'lon':lon,'nam':nam,'opy':opy,'out':out,'pol':pol,'rad':rad,'res':res,'rxh':rxh,
	'ter':ter,'tlt':tlt,'txh':txh,'uid':uid,'vbw':vbw}
	#print (args)
	print "Calculating '"+nam+"' out to "+rad+"km at "+res+"PPD..."
	r = requests.post(apiurl, data=args)
	print r.text
	download(r.text,nam)

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
	
# Open CSV file
with open('data.csv', 'rb') as csvfile:
	csvdata = csv.reader(csvfile, delimiter=',')
	for row in csvdata:
		if row[0].isdigit(): # Ignore Header row
			start_time = time.time() # Stopwatch start
			calculate(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],
			row[10],row[11],row[12],key,row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],uid,row[25])
			elapsed = time.time() - start_time # Stopwatch stop
			print "Elapsed time: "+str(elapsed)+"s"
			delay=1 # Minimum time between calcs is 10 seconds.
			if row[19] < 50: # If radius is less than 50km
				delay=5 # slow down or we might get ticked off for thrashing the server
			if row[19] < 20: # < 20km
				delay=8 # slow down some more...
			time.sleep(delay)
		
		
		