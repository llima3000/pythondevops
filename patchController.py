#!/usr/bin/python

import scp
import json
from paramiko import SSHClient
from scp import SCPClient
from time import sleep

host="10.91.55.11"
user="admin"
password="Avi123$%"
patch='controller_patch.17.2.9-3p2.pkg'

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(host, username=user, password=password)

scp = SCPClient(ssh.get_transport())
scp.put('../' + patch, remote_path='/tmp')

session = ssh.get_transport().open_session()
session.set_combine_stderr(True)
session.get_pty()
session.exec_command('shell')
stdin = session.makefile('wb', -1)
stdout = session.makefile('rb', -1)
stdin.write(user + '\n')
print(stdout.read().decode("utf-8"))
stdin.write(password + '\n')
print(stdout.read().decode("utf-8"))
stdin.write('patch system image_path /tmp/' + patch + '\n')
print(stdout.read().decode("utf-8"))
stdin.flush()

sleep(120)
session.close()
scp.close()
ssh.close()
