FROM ubuntu

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.7 \
    python3-pip  \
    chromium-browser \
    chromium-chromedriver 

RUN pip3 install \
	selenium \
	mysql-connector-python \
	requests

COPY * /Scraper/




