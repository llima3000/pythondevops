#!/bin/sh

echo "Type the controller IP address:"
read controller
echo "Type the admin name:"
read admin
stty_orig=`stty -g` # save original terminal setting.
stty -echo          # turn-off echoing.
echo "Type the admin password: "
read passwd         # read the password
stty $stty_orig     # restore terminal setting.

ansible-playbook baml_avi_playbook.yml -e "controller=$controller username=$admin password=$passwd"