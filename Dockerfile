from alpine

ENV UPDATE_FREQ=15

WORKDIR /root

RUN set -xe \
    && apk add -U python3 \
    && pip3.6 install dnspython docker \
    && rm -rf /var/cache/apk/*

COPY ./docker-swarm-dns.py /docker-swarm-dns.py

VOLUME /var/run/docker.sock

ENTRYPOINT ["/root/docker-swarm-dns.py"]
