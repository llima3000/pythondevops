#!/usr/bin/python

import scp
import json
from paramiko import SSHClient
from scp import SCPClient

host="10.91.55.11"
user="admin"
password="Avi123$%"

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(host, username=user, password=password)

scp = SCPClient(ssh.get_transport())
scp.put('../controller.17.2.11.pkg', remote_path='/tmp')

session = ssh.get_transport().open_session()
session.set_combine_stderr(True)
session.get_pty()
session.exec_command('sudo cp /tmp/controller.17.2.11.pkg /var/lib/avi/upgrade_pkgs/controller.pkg')
stdin = session.makefile('wb', -1)
stdout = session.makefile('rb', -1)
stdin.write(password + '\n')
stdin.flush()
print(stdout.read().decode("utf-8"))
session.close()
scp.close()
ssh.close()
