# -*- coding: utf-8 -*-
import datetime
import json
import urllib2
import os

def install_license(valid_user, valid_date, out_dir):
    today = datetime.date.today()
    begin_date = today.strftime('%Y-%m-%d')
    end_date = valid_date

    payload = {
        "nextgis_guid": "00000000-0000-0000-0000-0000000000000",
        "start_date": begin_date,
        "end_date": valid_date,
        "supported": "true"
    }

    url = 'http://192.168.250.1:9201/sign'
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(payload))
    data = json.load(response)
    sign = data['sign']

    # Create user and support info
    license_data = {
        'username': valid_user,
        'first_name': valid_user,
        'last_name': '',
        'nextgis_guid': "00000000-0000-0000-0000-0000000000000",
        'email': 'no-reply@nextgis.com',
        'supported': 'true',
        'sign': sign,
        'start_date': begin_date,
        'end_date': valid_date,
    }

    if not os.path.exists(lic_path):
        os.makedirs(lic_path) 
    lic_path = os.path.join(out_dir, 'license.json')
    with open(lic_path, 'w') as outfile:
        json.dump(license_data, outfile)
