#!/usr/bin/python

import sys
#import argparse
import json

from avi.sdk.avi_api import ApiSession
from avi.sdk.utils.api_utils import ApiUtils
from requests.packages import urllib3

urllib3.disable_warnings()

ip = "10.10.29.252"
username = "admin"
password = "Avi123$%"
tenant = "admin"

from_email = "avi@socgen.com"
search_domain = "socgen.com"
dnssrvlist = [{'addr': '8.8.8.8', 'type': 'V4'}, 
              {'addr': '8.8.4.4', 'type': 'V4'}]
ntpsrvlist = [{'server': {'addr': '0.us.pool.ntp.org', 'type': 'DNS'}},
              {'server': {'addr': '1.us.pool.ntp.org', 'type': 'DNS'}}]

sysconfigData = {
    'email_configuration': {
        'smtp_type': 'SMTP_LOCAL_HOST',
        'from_email': from_email
    },
    'global_tenant_config': {
        'se_in_provider_context': True,
        'tenant_access_to_provider_se': True,
        'tenant_vrf': False
    },
    'dns_configuration': {
        'search_domain': search_domain,
        'server_list': dnssrvlist
    },
    'portal_configuration': {
        'use_uuid_from_input': False,
        'redirect_to_https': True,
        'disable_remote_cli_shell': False,
        'enable_clickjacking_protection': True,
        'enable_http': True,
        'enable_https': True,
        'password_strength_check': True,
        'allow_basic_authentication': False
    },
    'ntp_configuration': {
        'ntp_servers': ntpsrvlist
    },
    'default_license_tier': 'ENTERPRISE_18'
}

api = ApiSession.get_session(controller_ip=ip, username=username, password=password, tenant=tenant, api_version='17.2.10')
systemconfiguration = api.put('systemconfiguration', data=json.dumps(sysconfigData))

print(systemconfiguration.status_code)
print(systemconfiguration.content)