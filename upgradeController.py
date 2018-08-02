#!/usr/bin/python

import json
from avi.sdk.avi_api import ApiSession

host="10.91.55.11"
user="admin"
password="Avi123$%"

# logon controller
api = ApiSession.get_session(controller_ip=host, username=user, password=password, api_version='17.2.10')

jsonData = {"image_path": "controller://upgrade_pkgs/"}

systemconfiguration = api.post('cluster/upgrade', data=json.dumps(jsonData))

print(systemconfiguration.status_code)
print(systemconfiguration.content)
