##############################################################
# Copyright (c) 2018 MindTheVirt, Inc. All rights reserved.  #
#                     -- @MindTheVirt --                     #
##############################################################


import json
import requests
from datetime import datetime

startTime = datetime.now()

# retrieve config for pipedrive and zendesk

with open('config.json') as config:
    data = json.load(config)
    zenuser = data['zendesk']['username']
    zenapi = data['zendesk']['apikey']
    pipeapi = data['pipedrive']['apikey']
    orgurl = data['zendesk']['orgurl']
    enduserurl = data['zendesk']['enduserurl']

# zendesk authentication
user = zenuser + '/token'
pwd = zenapi

urls = []
urls.append(orgurl)
urls.append(enduserurl)
for url in urls:
    response = requests.get(url, auth=(user, pwd))
    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting')
        exit()

# get organizaitons from pipedrive and create them in zendesk
startnum = 0
limitnum = 50

print "Start sync of organizations from pipedrive to zendesk"

while True:
    response = requests.get('https://api.pipedrive.com/v1/organizations?start=0&api_token=%s&start=%s&limit=%s' % (pipeapi, startnum, limitnum))
    orgdata = response.json()
    organizations = orgdata['data']
    # For each company, try to create it in zendesk
    if organizations:
        for i in organizations:
            data = {"organization": {"name": i['name']}}
            payload = json.dumps(data)
            headers = {'content-type': 'application/json'}
            response = requests.post(orgurl, data=payload, auth=(user, pwd), headers=headers)
            if response.status_code == 201:
                print "%s has been created" % i['name']
        startnum = startnum + 50
        limitnum = limitnum + 50
    else:
        print "Synchronized all organizations from pipedrive to zendesk"
        break


# get persons from pipedrive and create users in zendesk
startnum = 0
limitnum = 50

print "Start sync of persons from pipedrive to zendesk"

while True:
    response = requests.get('https://api.pipedrive.com/v1/persons?start=0&api_token=%s&start=%s&limit=%s' % (pipeapi, startnum, limitnum))
    personsdata = response.json()
    persons = personsdata['data']
    if persons:
        for p in persons:
            if p['org_id'] and p['email'][0]['value']:
                data = {"user": {"name": p['name'], "email": p['email'][0]['value'], "organization": {"name": p['org_id']['name']}}}
                payload = json.dumps(data)
                headers = {'content-type': 'application/json'}
                response = requests.post(enduserurl, data=payload, auth=(user, pwd), headers=headers)
                if response.status_code == 201:
                    print "%s has been created under %s" % (p['name'], p['org_id']['name'])
        startnum = startnum + 50
        limitnum = limitnum + 50
    else:
        print "Synchronized all contacts from pipedrive to zendesk"
        break

runtime = datetime.now() - startTime
print 'Sync took %s' % runtime
