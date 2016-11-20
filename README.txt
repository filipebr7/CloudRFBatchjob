CloudRF API clients

These scripts allow you to process a spreadsheet of sites with the CloudRF API.
To use it you will need a CloudRF account and Python. Google earth is not essential.
Your CloudRF API credentials can be obtained by emailing support@cloudrf.com or looking up your UID in the URL immediately after you login eg. /user/16322/ and creating a SHA1 hash of your password for your key.
You need to edit your data to add your UID and KEY in the 'uid' and 'key' fields.

Concept:
The scripts read in data from a CSV file, then perform HTTP POST requests to https://cloudrf.com/API/api.php for coverage and /API/ppa/ppa.php for path profile. 
The result can be a KMZ URL, a HTML snippet or a image bounds as decimal degrees. See the API documentation for more information on how to set the format.

Upon completion of each row, the script requests a mesh be created which stitches processed calculations into a super layer which is also downloaded as a KMZ.
The 'net' field is used for the network name so set this carefully if you plan to mesh sites later on. You can mesh multiple networks in one run eg. NET-A, NET-B.

Usage:
Path profile: python pathprofile.py pathprofile.csv
Coverage: python coverage.py coverage.csv

API reference:
The entire API is available at https://cloudrf.com/docs/api

Support:
Email support@cloudrf.com
 
