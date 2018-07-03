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

session = ssh.get_transport().open_session()
session.set_combine_stderr(True)
session.get_pty()
session.exec_command('sudo cp /tmp/controller_patch.pkg /var/lib/avi/upgrade_pkgs/')
stdin = session.makefile('wb', -1)
stdout = session.makefile('rb', -1)
stdin.write(password + '\n')
stdin.flush()
print(stdout.read().decode("utf-8"))
session.close()
scp.close()
ssh.close()

# logon controller
api = ApiSession.get_session(controller_ip=host, username=user, password=password, api_version='17.2.10')

jsonData = {"image_path": "controller://upgrade_pkgs/"}

systemconfiguration = api.post('cluster/upgrade', data=json.dumps(jsonData))

print(systemconfiguration.status_code)
print(systemconfiguration.content)
