REQUIRED:
Admin Oauth Key & Admin Fingerprint. Please use this guide to get them:
https://synapsefi.atlassian.net/wiki/spaces/PRODENG/pages/199393484/Obtaining+OAuth+Key+and+Fingerprint+from+Dashboards

Files:
input.csv - Here you will supply the transacitons you wish to run (Check dispute statuses for)
output.csv - This is the file that will output once all transactions are checked
app.py - The python file that does everything 

How To Run:
1. Get your admin OAuth_Key & Admin_Fingerprint and supply it on lines 5 & 6
Example: 
admin_oauth="<<admin_oauth>>"
admin_fp="<<admin_fp>>"

Should be:
admin_oauth="admin_oauth_key_123456789abcdefghij"
admin_fp="123456789abcdefghij"

(Alternatively, you can leave it as is and will be prompted to enter them if the default values are left)

2. Enter the transactions you wish to lookup in the 'id' fieldname on input.csv

3. Open a terminal in the same directory of this app and run:
python3 app.py

