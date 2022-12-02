#!/bin/bash

# Written Assignment Phase Req#92534 ISL 27R – Full Stack Developer
# Run this file to start the web application
# Then please open a browser and access http://localhost:8027

# Set config files
cp cfg/nginx.conf.tmpl cfg/nginx.conf
cp cfg/config.yaml.tmpl cfg/config.yaml

# Call shell script to modify config files
# docker exec -it vdocker sh -c "chmod +x /vdisk/compose/execute.sh"
# docker exec -d vdocker sh -x "/vdisk/compose/execute.sh"

# Another way
ipaddress=$(docker network inspect vdocker_default | grep "IPv4Address" | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}")
# ipaddress=$(docker inspect vdocker | grep "IPAddress" | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}")
docker exec -it vdocker sh -c "sed -i 's/192.168.0.17/'${ipaddress}'/g' /vdisk/cfg/config.yaml"
docker exec -it vdocker sh -c "sed -i 's/192.168.0.17/'${ipaddress}'/g' /vdisk/cfg/nginx.conf"

# Build docker image
docker exec -it vdocker sh -c "docker build -t py3web -f /vdisk/compose/Dockerfile /vdisk/compose"

# Run all containers
docker exec -it vdocker sh -c "chmod +x /vdisk/server/main.wsgi"
docker exec -it vdocker sh -c "docker-compose -f /vdisk/compose/docker-compose.yaml up"
