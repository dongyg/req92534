#!/bin/bash

# Written Assignment Phase Req#92534 ISL 27R – Full Stack Developer
# Run this file to start the web application
# Then please open a browser and access http://localhost:8027

# Set config files
cp cfg/nginx.conf.tmpl cfg/nginx.conf
cp cfg/config.yaml.tmpl cfg/config.yaml
docker exec -d vdocker sh -x "/vdisk/compose/execute.sh"

# Ensure can execute
docker exec -it vdocker sh -c "chmod +x /vdisk/compose/execute.sh"
docker exec -it vdocker sh -c "chmod +x /vdisk/server/main.wsgi"

# Build docker image
docker exec -it vdocker sh -c "docker build -t py3web -f /vdisk/compose/Dockerfile /vdisk/compose"

# Run all containers
docker exec -it vdocker sh -c "docker-compose -f /vdisk/compose/docker-compose.yaml up"
