FROM python:3.8-slim-buster

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

RUN apt-get update; \
	apt-get install -q -y --no-install-recommends default-libmysqlclient-dev fcgiwrap; \
	\
	rm -rf /var/lib/apt/lists/*;

WORKDIR /approot
