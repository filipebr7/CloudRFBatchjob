CloudRF Batchjob

This Python script automates the generation of radio propagation calculations using the CloudRF API.
To use it you will need a CloudRF account, Python and Google earth.
Your CloudRF API credentials can be obtained by emailing support@cloudrf.com

Concept:
The script reads in data from the CSV file, then performs a HTTP POST request to https://web.cloudrf.com for each row. 
The result is a link to a KMZ file which the script downloads. 
It can also optionally open the KMZ in Google earth as it goes by setting 'googlearth=1' flag at the top of the script.

Upon completion of each row, the script requests a mesh be created which stitches processed calculations 
into a super layer which is also downloaded as a KMZ.


API reference:
The entire API is available at https://web.cloudrf.com/docs/api

Support:
Email support@cloudrf.com
 
