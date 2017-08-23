from alpine

ENV PYTHONUNBUFFERED=0

WORKDIR /root

RUN set -xe \
    && apk add -U python3 \
    && pip3.6 install dnspython docker \
    && rm -rf /var/cache/apk/*

COPY ./docker-swarm-dns.py /root/docker-swarm-dns.py

RUN ["chmod", "+x", "/root/docker-swarm-dns.py"]

ENTRYPOINT ["/root/docker-swarm-ddns.py"]
