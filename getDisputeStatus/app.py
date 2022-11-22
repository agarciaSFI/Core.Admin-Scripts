import csv, requests, json, time


admin_oauth="<<admin_oauth>>"
admin_fp="<<admin_fp>>"


PROD_TRANS_SHOW = "https://silent-wildflower-5960.synapsefi.com/trans/show"
HEADERS={'content-type':"application/json"}
#Check Credentials First
print("Checking Admin Dashboard Credentails...")
if admin_oauth == "<<admin_oauth>>" or admin_fp == "<<admin_fp>>":
    admin_oauth = input("No Credentials Detected on Line 4-5, Please enter your Admin OAuth Key \n(Ref: synapsefi.atlassian.net/wiki/spaces/PRODENG/pages/199393484/Obtaining+OAuth+Key+and+Fingerprint+from+Dashboards)\nAdmin Oauth: ")
    admin_fp = input("Please enter your Admin Fingerprint: ")
    print("Checking Credentials...")
    body = {"login":{"oauth_key":admin_oauth},"user":{"fingerprint":admin_fp},"filter":{"page":1,"query":"637bee8cc4298d2b0763f881"}}
    try:
        response = requests.post(PROD_TRANS_SHOW,json=body,headers=HEADERS)
    except:
        print("Error with input. Please check and try again")
        quit()
else:
    body = {"login":{"oauth_key":admin_oauth},"user":{"fingerprint":admin_fp},"filter":{"page":1,"query":"637bee8cc4298d2b0763f881"}}
    try:
        response = requests.post(PROD_TRANS_SHOW,json=body,headers=HEADERS)
    except:
        print("Error with credentials on lines 4 or 5. Please check them and try again.  \n(Ref: synapsefi.atlassian.net/wiki/spaces/PRODENG/pages/199393484/Obtaining+OAuth+Key+and+Fingerprint+from+Dashboards)")
        quit()
pretty_response = json.loads(response.text)
if pretty_response['http_code'] == "200":
    print("Credential Check Successful!")
elif pretty_response['http_code'] == "401":
    print("Credentials Are Invalid. Please Try again. \n(Ref: synapsefi.atlassian.net/wiki/spaces/PRODENG/pages/199393484/Obtaining+OAuth+Key+and+Fingerprint+from+Dashboards)")
    quit()
#END oF Check Credentials First

#GET DATA FROM CSV & Add to fromFile Array
csvFilePath = "input.csv"

fromFile = []
errors=[]
with open(csvFilePath, encoding='utf-8') as csvf:
    csvReader = csv.DictReader(csvf)
    print("Getting Transactions From Input File & Storing In Memory...")
    for rows in csvReader:
        fromFile.append(rows['id']) #add transaciton ID to FromFile array once data has been obtained for the row
print("Done Getting Data From CSV: "+csvFilePath+" Getting Transaction From Admin Dashboard & Writing to CSV...")
#END OF GET DATA FROM CSV & Add to fromFile Array

#Get Trans Key Values & Write To CSV
with open('output.csv','w') as csv_file: #Createnew csv file to write to
    fieldnames = ['Reversed','Reverse_Date','id',"client","From","amount","currency","creation","dispute_reason","dispute_status","dispute_status_note","provisional_credit_transaction_id","dispute_form"]#Fieldnames
    output = csv.DictWriter(csv_file, fieldnames=fieldnames)
    output.writeheader()

    #Go through all FromFile array
    for index1, item1 in enumerate(fromFile):
        body = {"login":{"oauth_key":admin_oauth},"user":{"fingerprint":admin_fp},"filter":{"page":1,"query":item1}}
        try:
            response = requests.post(PROD_TRANS_SHOW,json=body,headers=HEADERS)
        except:
            print("Error with getting Transaction: "+item1+" from the dashboard. Please Check It & Try Again")
            quit()
        pretty_response = json.loads(response.text)
        for index2, item2 in enumerate(pretty_response['trans']):#enter trans array from GET TRANS response

            #TRY each key before writing to csv to debug failed cases
            try:
                r = dict(id=item2['_id']['$oid'])
            except KeyError:
                e = ("Key Error When attempting to get _id.$oid from trx: "+item1+" Please confirm the transaction has this Key in Admin Dashboard.Skipping...")
                errors.append(e)
                print(e)
                continue
            try:
                r = dict(client=item2['client']['name'])
            except KeyError:
                e = ("Key Error When attempting to get client.name from trx: "+item1+" Please confirm the transaction has this Key in Admin Dashboard.Skipping...")
                errors.append(e)
                print(e)
                continue
            try:
                r = dict(From=item2['from']['user']['legal_names'][0])
            except KeyError:
                e = ("Key Error When attempting to get from.user.legal_names.[0] from trx: "+item1+" Please confirm the transaction has this Key in Admin Dashboard.Skipping...")
                errors.append(e)
                print(e)
                continue
            try:
                r = dict(amount=item2['amount']['amount'])
            except KeyError:
                e = ("Key Error When attempting to get amount.amount from trx: "+item1+" Please confirm the transaction has this Key in Admin Dashboard.Skipping...")
                errors.append(e)
                print(e)
                continue
            try:
                r = dict(currency=item2['amount']['currency'])
            except KeyError:
                e = ("Key Error When attempting to get amount.currency from trx: "+item1+" Please confirm the transaction has this Key in Admin Dashboard.Skipping...")
                errors.append(e)
                print(e)
                continue
            try:
                r = dict(creation=time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime(item2["extra"]["created_on"]['$date']/1000 )))
            except KeyError:
                e = ("Key Error When attempting to get extra.created_on.$date from trx: "+item1+" Please confirm the transaction has this Key in Admin Dashboard.Skipping...")
                errors.append(e)
                print(e)
                continue
            try:
                r = dict(dispute_reason=item2['extra']['other']['dispute_reason'])
            except KeyError:
                e = ("Key Error When attempting to get extra.other.dispute_reason from trx: "+item1+" Please confirm the transaction has this Key in Admin Dashboard.Skipping...")
                errors.append(e)
                print(e)
                continue
            try:
                r = dict(dispute_status=item2['extra']['other']['dispute_meta']['dispute_status'])
            except KeyError:
                e = ("Key Error When attempting to get extra.other.dispute_meta.dispute_status from trx: "+item1+" Please confirm the transaction has this Key in Admin Dashboard.Skipping...")
                errors.append(e)
                print(e)
                continue
            try:
                r = dict(dispute_status_note=item2['extra']['other']['dispute_meta']['dispute_status_note'])
            except KeyError:
                e = ("Key Error When attempting to get extra.other.dispute_meta.dispute_status_note from trx: "+item1+" Please confirm the transaction has this Key in Admin Dashboard.Skipping...")
                errors.append(e)
                print(e)
                continue
            try:
                r = dict(provisional_credit_transaction_id=item2['extra']['other']['dispute_meta']['provisional_credit_transaction_id'])
            except KeyError:
                e = ("Key Error When attempting to get extra.other.dispute_meta.provisional_credit_transaction_id from trx: "+item1+" Please confirm the transaction has this Key in Admin Dashboard.Skipping...")
                errors.append(e)
                print(e)
                continue
            try:
                r = dict(dispute_form=item2['extra']['other']['dispute_meta']['dispute_form'])
            except KeyError:
                e = ("Key Error When attempting to get extra.other.dispute_meta.dispute_form from trx: "+item1+" Please confirm the transaction has this Key in Admin Dashboard.Skipping...")
                errors.append(e)
                print(e)
                continue
            #if PC provided, check if it has been returned to determine 'Reversed','Reverse Date'
            Tr = None
            Tc = None
            if item2['extra']['other']['dispute_meta']['provisional_credit_transaction_id'] != None:
                body2 = {"login":{"oauth_key":admin_oauth},"user":{"fingerprint":admin_fp},"filter":{"page":1,"query":item2['extra']['other']['dispute_meta']['provisional_credit_transaction_id']}}
                response2 = requests.post(PROD_TRANS_SHOW,json=body2,headers=HEADERS)
                pretty_response2 = json.loads(response2.text)
                if pretty_response2['trans'][0]['recent_status']['status_id']=="6":
                    Tr = "TRUE",
                    Tc = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime(pretty_response2["trans"][0]["recent_status"]['date']['$date']/1000 ))
                   
            #Write to csv now that data has been checked for Key Errors
            r = dict(
                id=item2['_id']['$oid'],
                client=item2['client']['name'],
                From=item2['from']['user']['legal_names'][0],
                amount=item2['amount']['amount'],
                currency=item2['amount']['currency'],
                creation=time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime(item2["extra"]["created_on"]['$date']/1000 )),
                dispute_reason=item2['extra']['other']['dispute_reason'],
                dispute_status=item2['extra']['other']['dispute_meta']['dispute_status'],
                dispute_status_note=item2['extra']['other']['dispute_meta']['dispute_status_note'],
                provisional_credit_transaction_id=item2['extra']['other']['dispute_meta']['provisional_credit_transaction_id'],
                dispute_form=item2['extra']['other']['dispute_meta']['dispute_form'],
                Reversed = Tr,
                Reverse_Date = Tc
            )
            output.writerow(r)
            print("Succsesfully Wrote Data For: "+str(r))
    
print("Done! Please see output.csv for results! Failed Transaction log:\n "+str(errors))
