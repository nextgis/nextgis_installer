# -*- coding: utf-8 -*-
import datetime
import json
import base64
import os, sys
if sys.version_info[0] >= 3:
    from urllib.request import Request, urlopen
else:
    from urllib2 import Request, urlopen


def install_license(valid_user, valid_date, out_dir, sign_pwd):
    today = datetime.date.today()
    begin_date = today.strftime('%Y-%m-%d')
    end_date = valid_date

    payload = {
        "nextgis_guid": "00000000-0000-0000-0000-0000000000000",
        "start_date": begin_date,
        "end_date": end_date,
        "supported": "true"
    }

    url = 'https://s1.nextgis.com/api/sign'
    req = Request(url)
    if sign_pwd is not None:
        base64string = base64.b64encode(sign_pwd)
        req.add_header("Authorization", "Basic %s" % base64string)   
    req.add_header('Content-Type', 'application/json')
    response = urlopen(req, json.dumps(payload))
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
        'end_date': end_date,
    }

    if not os.path.exists(out_dir):
        os.makedirs(out_dir) 
    lic_path = os.path.join(out_dir, 'license.json')
    with open(lic_path, 'w') as outfile:
        json.dump(license_data, outfile)
