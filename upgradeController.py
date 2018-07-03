#!/usr/bin/python

import scp
import json
from paramiko import SSHClient
from scp import SCPClient
from avi.sdk.avi_api import ApiSession

host="10.91.55.5"
user="admin"
password="Avi123$%"

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(host, username=user, password=password)

scp = SCPClient(ssh.get_transport())
scp.put('../../17.2.11-1p1/controller_patch.pkg', remote_path='/tmp')
ssh.exec_command('sudo cp /tmp/ /var/lib/avi/upgrade_pkgs/')
scp.close()

# logon controller
api = ApiSession.get_session(controller_ip=host, username=user, password=password, api_version='17.2.10')

jsonData = {"image_path": "controller://upgrade_pkgs/"}

systemconfiguration = api.post('cluster/upgrade', data=json.dumps(jsonData))

print(systemconfiguration.status_code)
print(systemconfiguration.content)
