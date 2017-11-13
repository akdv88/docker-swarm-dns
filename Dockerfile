from alpine

ENV PYTHONUNBUFFERED=0

WORKDIR /root

RUN set -xe \
    && apk add --no-cache python3 \
    && pip3.6 install dnspython docker

COPY ./swarm-ddns.py /root/swarm-ddns.py

RUN ["chmod", "+x", "/root/swarm-ddns.py"]

ENTRYPOINT ["/root/swarm-ddns.py"]
