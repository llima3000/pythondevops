#!/usr/bin/python

#import argparse
import json

from time import sleep, time, timezone
from avi.sdk.avi_api import ApiSession
from avi.sdk.utils.api_utils import ApiUtils
from requests.packages import urllib3

urllib3.disable_warnings()

ip = "10.10.29.252"
username = "admin"
password = "Avi123$%"
tenant = "admin"
api_version= "17.2.7"
vcenter_url= "10.10.2.10"
vcenter_user="root"
vcenter_pwd="vmware"
discovery_time=750
vmware_cloud_name="vmwarecloud"
cloud_datacenter= "10GTest"
vmware_cluster_name="Arista"
vm_mgmt_nw_name="PG-1055"
vm_mgmt_nw_addr="10.91.55.0"
vm_mgmt_maskbits="24"
vm_mgmt_begin_addr="10.91.55.100"
vm_mgmt_end_addr="10.91.55.200"
vm_mgmt_dg="10.91.55.1"
vrf_gw_mon_ip="10.91.29.1"
vrf_name="VRF-GSLB"
prefix_name="luiz"
vcenter_folder="luiz"
network_name="PG-1029"
net_address="10.91.29.0"
net_maskbits="24"
beg_addr="10.91.55.101"
end_addr="10.91.55.250"
service_engine_group_name="SEGGSLB"

api = ApiSession.get_session(controller_ip=ip, username=username, password=password, tenant=tenant, api_version='17.2.10')

jsondata = {"vtype":"CLOUD_VCENTER",
            "prefer_static_routes":False,
            "enable_vip_static_routes":False,
            "state_based_dns_registration":True,
            "mtu":1500,
            "dhcp_enabled":False,
            "license_type":"LIC_CORES",
            "license_tier":"ENTERPRISE_18",
            "name":vmware_cloud_name,
            "vcenter_configuration": {
                "privilege":"WRITE_ACCESS",
                "username":vcenter_user,
                "vcenter_url":vcenter_url,
                "password":vcenter_pwd,
                "datacenter":cloud_datacenter }
            }

response = api.get('cloud/?name=' + vmware_cloud_name)

#exit(0)
if response.status_code == 200:
    resobj = json.loads(response.content)
    
    if resobj['count'] < 1:
        print("Creating new cloud")
        response = api.post('cloud', data=json.dumps(jsondata))
    else:
        print("Changing cloud config")
        response = api.put('cloud/' + resobj['results'][0]['uuid'], data=json.dumps(jsondata))

sleep(100)

# Create VRF
jsondata = {"name":"management",
        "tenant_ref": "/api/tenant/?name="+ tenant,
        "cloud_ref": "/api/cloud/?name=" + vmware_cloud_name,
        "system_default": True,
        "static_routes":[  {"route_id":"1",
                            "prefix": {"ip_addr": { "addr": "0.0.0.0", "type": "V4"}, "mask":0 },
                            "next_hop": {"addr":vm_mgmt_dg, "type": "V4"}
                            }]
        }

response = api.get('vrfcontext/?name=management')

if response.status_code == 200:
    resobj = json.loads(response.content)

print(response.status_code)
print(response.content)

exit(0)

print("VRF Admin Creation")
response = api.put_by_name('vrfcontext', "management", data=json.dumps(jsondata))
print(response.status_code)

# Configure Admin Network Obj
jsondata = { "name": vm_mgmt_nw_name,
        "vrf_context_ref": "/api/vrfcontext/?name=" + vrf_name,
        "tenant_ref": "/api/tenant/?name="+ tenant,
        "cloud_ref": "/api/cloud/?name=" + vmware_cloud_name,
        "exclude_discovered_subnets": False,
        "vimgrnw_ref": "/api/vimgrnwruntime/?name=" + vm_mgmt_nw_name,
        "dhcp_enabled": False,
        "configured_subnets": [
            {   "prefix": { "ip_addr": { "addr": vm_mgmt_nw_addr, "type": "V4" }, "mask": vm_mgmt_maskbits },
                "static_ranges": [
                    { "begin": { "addr": vm_mgmt_begin_addr, "type": "V4" },
                      "end": { "addr": vm_mgmt_end_addr, "type": "V4" }}
                ]
            }
        ],
        "discovery": { "ip_subnet": []}
    }

print("Admin Network Creation")
response = api.put_by_name('network', vm_mgmt_nw_name, data=json.dumps(jsondata))
print(response.status_code)

# Cloud connector update
json = {"name": vmware_cloud_name,
        "vcenter_configuration": {
            "management_network": "/api/vipgnameinfo/" + response['uuid'],
            "selected_subnet": vm_mgmt_nw_addr + "/" + vm_mgmt_maskbits,
            "management_ip_subnet": { "ip_addr": { "addr": vm_mgmt_nw_addr, "type": "V4" }, "mask": vm_mgmt_maskbits }
            }
        }
#response = api.patch("cloud/"+uuid, data=jsib.dumps(json)_)
