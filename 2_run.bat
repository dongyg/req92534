REM Written Assignment Phase Req#92534 ISL 27R – Full Stack Developer
REM Run this file to start the web application
REM Then please open a browser and access http://localhost:8027

REM Set config files
copy .\cfg\nginx.conf.tmpl .\cfg\nginx.conf
copy .\cfg\config.yaml.tmpl .\cfg\config.yaml

REM Call shell script to modify config files
REM docker exec -it vdocker sh -c "chmod +x /vdisk/compose/execute.sh"
REM docker exec -d vdocker sh -x "/vdisk/compose/execute.sh"

REM Another way
for /F %%i in ('docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" vdocker') do ( set ipaddress=%%i)

docker exec -it vdocker sh -c "sed -i 's/192.168.0.17/'%ipaddress%'/g' /vdisk/cfg/config.yaml"
docker exec -it vdocker sh -c "sed -i 's/192.168.0.17/'%ipaddress%'/g' /vdisk/cfg/nginx.conf"

REM Build docker image
docker exec -it vdocker sh -c "docker build -t py3web -f /vdisk/compose/Dockerfile /vdisk/compose"

REM Run all containers
docker exec -it vdocker sh -c "chmod +x /vdisk/server/main.wsgi"
docker exec -it vdocker sh -c "docker-compose -f /vdisk/compose/docker-compose.yaml up"
