#!/usr/bin/env python3.6

from time import sleep
import argparse, \
       ast, \
       docker, \
       dns.resolver, \
       dns.query, \
       dns.tsigkeyring, \
       dns.update, \
       os, \
       sys

parser = argparse.ArgumentParser()
parser.add_argument("-s",help="list of ip address[es] of your swarm nodes. Format: ipaddress,..",required=True)
parser.add_argument("-n",help="your dnserver[s] configuration. Format: \"{'name':{'ip':'youripaddress','key':'yourupdatekey}}\"",required=True)
parser.add_argument("-d",help="your domain name (example.)",required=True)
parser.add_argument("-u",help="update frequency in seconds",type=int,required=True)
args = parser.parse_args()

swnodes = args.s.split(',')
dnservers = ast.literal_eval(args.n)
domain = args.d
ttl = args.u

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
                    dns_add(svc.replace('_','-').lower())
            if rm:
                print('DEL', rm)
                for svc in rm:
                    dns_remove(svc.replace('_','-').lower())
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
