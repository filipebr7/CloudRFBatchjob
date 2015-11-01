CloudRF Batchjob

This Python script automates the generation of radio propagation calculations using the CloudRF API.
To use it you will need a CloudRF account and Python. Google earth is not essential.
Your CloudRF API credentials can be obtained by emailing support@cloudrf.com or looking up your UID in the URL immediately after you login eg. /user/16322/ and creating a SHA1 hash of your password for your key.

Concept:
The script reads in data from the CSV file, then performs a HTTP POST request to https://cloudrf.com/API/api.php for each row. 
The result is a link to a KMZ file which the script downloads. 
It can also optionally open the KMZ in Google earth as it goes by setting 'googlearth=1' flag at the top of the script.

Upon completion of each row, the script requests a mesh be created which stitches processed calculations into a super layer which is also downloaded as a KMZ.
The 'net' field is used for the network name so set this carefully if you plan to mesh sites later on. You can mesh multiple networks in one run eg. NET-A, NET-B.


API reference:
The entire API is available at https://web.cloudrf.com/docs/api

Support:
Email support@cloudrf.com
 
