#!/usr/bin/python
import yaml

cloud_name = "Default-Cloud"

csvfilename = "VIP_Master_List.csv"
ymlfilenamein = "output/avi_config_create_object.yml"
ymlfilenameout = "baml_avi_playbook.yml"

with open(ymlfilenamein, "rb") as f:
    yamldata = yaml.load(f)

csvfile = open(csvfilename, "r")
ymlfile = open(ymlfilenameout, "w")

line = csvfile.readline()
while line != "":
    csvlist = line.split(",")
    for task in yamldata[0]['tasks']:
        if "avi_virtualservice" in task:
            if task["avi_virtualservice"]["name"] == csvlist[12]:
                strOutput = "Changing VS: " + csvlist[12] + " | SEGROUP: " + csvlist[11]
                print("")
                task["avi_virtualservice"]["cloud_ref"] = "/api/cloud?name=" + cloud_name
                task["avi_virtualservice"]["se_group_ref"] = "/api/serviceenginegroup/?name=" + csvlist[11]
                if csvlist[17] == "No":
                    task["avi_virtualservice"]["use_vip_as_snat"] = True
                    strOutput = strOutput +" | use_vip_as_snat: True"
                print(strOutput)
    line = csvfile.readline() 

print("")
#print(yaml.dump(yamldata, default_flow_style=False))
ymlfile.writelines(yaml.dump(yamldata, default_flow_style=False))
ymlfile.close()
csvfile.close()