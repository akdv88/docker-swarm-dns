#!/usr/bin/env python3.6

from time import sleep
import docker, \
       dns.resolver, \
       dns.query, \
       dns.tsigkeyring, \
       dns.update, \
       os, \
       sys

swnodes = ['192.168.15.201','192.168.15.202','192.168.15.203','192.168.15.204','192.168.15.205']
dnservers = {'master':{'ip':'192.168.2.6','key':'EMtUbnXU3as1Eczq2bVZ8g=='},'slave':{'ip':'192.168.2.7','key':'ctWc6TO3tD9YMV1QYgh9Jg=='}}
domain = 'subsident.docker.'
ttl = int(os.environ['UPDATE'])

def docker_query():
    conn = docker.from_env()
    serv_pre = set()
    while True:
        serv_cur = set()
        for service in conn.services.list():
            if 'add.dns' in service.attrs['Spec']['Labels']:
                if service.attrs['Spec']['Labels']['add.dns'] == 'true':
                    serv_cur.add(service.name)
        if serv_pre != serv_cur:
            add = serv_cur.difference(serv_pre)
            rm = serv_pre.difference(serv_cur)
            if add:
                print('ADD', add)
                for svc in add:
                    dns_add(svc)
            if rm:
                print('DEL', rm)
                for svc in rm:
                    dns_remove(svc)
        serv_pre = serv_cur
        sleep(ttl)

def dns_add(svc):
    for host, conf in dnservers.items():
        print('Add DNS Record \''+svc+'\' sent to',host,'dnserver ('+conf['ip']+')')
        keyring = dns.tsigkeyring.from_text({
                'rndc-key.' : conf['key']
                })
        update = dns.update.Update(domain, keyring=keyring)
        for swip in swnodes:
            update.add(svc, 15, 'a', swip)
            resp = dns.query.tcp(update, conf['ip'])
def dns_remove(svc):
    for host, conf in dnservers.items():
        print('Remove DNS Record \''+svc+'\' sent to',host,'dnserver ('+conf['ip']+')')
        keyring = dns.tsigkeyring.from_text({
                'rndc-key.' : conf['key']
                })
        update = dns.update.Update(domain, keyring=keyring)
        update.delete(svc, 'a')
        resp = dns.query.tcp(update, conf['ip'])

if __name__ == "__main__":
    docker_query()
