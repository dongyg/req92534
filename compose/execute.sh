#!/bin/bash

# Set config files
sed -i 's/192.168.0.17/'$(hostname -i)'/g' /vdisk/cfg/config.yaml
sed -i 's/192.168.0.17/'$(hostname -i)'/g' /vdisk/cfg/nginx.conf
