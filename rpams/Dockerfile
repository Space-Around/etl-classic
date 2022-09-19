FROM python:3.10-alpine

#COPY ./requirements.txt /opt/rpams/requirements.txt

RUN apk update
RUN apk add build-base
RUN apk add alpine-sdk
# RUN python3 -m pip install -r /opt/rpams/requirements.txt
RUN apk add zlib-dev jpeg-dev gcc musl-dev
RUN pip install mitmproxy
RUN pip install sqlalchemy
RUN pip install requests

COPY . /opt/rpams/
WORKDIR /opt/rpams/

RUN chmod +x /opt/rpams/mitm/mitmdump

EXPOSE 8081

curl --header "Content-Type: application/json" --request POST --data '{"command":"ls -la"}' http://0.0.0.0:8082/exec