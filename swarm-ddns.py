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
args = parser.parse_args()

swnodes = args.s.split(',')
dnservers = ast.literal_eval(args.n)
domain = args.d

def docker_int():
    svc_list = {}
    try:
        conn = docker.from_env()
    except:
        print("Error: No connection to docker socket!")
# Initialization
    for service in conn.services.list():
        if 'add.dns' in service.attrs['Spec']['Labels']:
            svc = service.attrs['Spec']['Labels']['add.dns']
            svc_list[service.attrs['Spec']['Name']] = svc
            print('\nService/Action:', service.attrs['Spec']['Name']+'/add(update)')
            try:
                dns_add(svc.replace('_','-').lower())
            except:
                print("...Error: DNS update failed!")
# Event Listener
    for event in conn.events('','','','true'):
        svc_id = event['Actor']['ID']
        if event['Type'] == 'service' and (event['Action'] == 'create' or event['Action'] == 'update'):
            svc_name = conn.services.get(svc_id).attrs['Spec']['Name']
            if 'add.dns' in conn.services.get(svc_id).attrs['Spec']['Labels']:
                svc = conn.services.get(svc_id).attrs['Spec']['Labels']['add.dns']
                print('\nService/Action:', svc_name+'/'+event['Action'])
                if event['Action'] == 'create' or (event['Action'] == 'update' and svc_name not in svc_list):
                    try:
                        dns_add(svc.replace('_','-').lower())
                    except:
                        print("...Error: DNS update failed!")
                elif event['Action'] == 'update' and svc_name in svc_list:
                    if svc_list[svc_name] != svc:
                        svc_old = svc_list[svc_name]
                        try:
                            dns_remove(svc_old.replace('_','-').lower())
                        except:
                            print("...Error: DNS update failed!")
                        try:
                            dns_add(svc.replace('_','-').lower())
                        except:
                            print("...Error: DNS update failed!")
                    else:
                        print('Nothing to do. Service domain name did not changed')                     
                svc_list[svc_name] = svc 
            elif 'add.dns' not in conn.services.get(svc_id).attrs['Spec']['Labels'] and event['Action'] == 'update' and svc_name in svc_list:
                svc_old = svc_list[svc_name]
                print('\nService/Action:', svc_name+'/'+event['Action'])
                try:
                    dns_remove(svc_old.replace('_','-').lower())
                except:
                    print("...Error: DNS update failed!")
                svc_list.pop(svc_name)
        elif event['Type'] == 'service' and event['Action'] == 'remove':
            svc_name = event['Actor']['Attributes']['name']
            svc = svc_list[svc_name]
            svc_list.pop(svc_name)
            print(svc_list)
            print('\nService/Action:', svc_name+'/'+event['Action'])
            try:
                dns_remove(svc.replace('_','-').lower())
            except:
                print("...Error: DNS update failed!")
# DDNS Queries
def dns_add(svc):
    for host, conf in dnservers.items():
        print('Add/Update DNS Record \''+svc+'\' sent to',host,'dnserver ('+conf['ip']+')',end='')
        keyring = dns.tsigkeyring.from_text({
                'rndc-key.' : conf['key']
                })
        check_record = dns.update.Update(domain, keyring=keyring)
        check_record.absent(svc)
        resp_check = dns.query.tcp(check_record, conf['ip'])
        if resp_check.rcode() == 6:
            dns_query_status(resp_check.rcode())
            continue
        update = dns.update.Update(domain, keyring=keyring)
        for swip in swnodes:
            update.add(svc, 15, 'a', swip)
            resp = dns.query.tcp(update, conf['ip'])
        dns_query_status(resp.rcode())

def dns_remove(svc):
    for host, conf in dnservers.items():
        print('Remove DNS Record \''+svc+'\' sent to',host,'dnserver ('+conf['ip']+')',end='')
        keyring = dns.tsigkeyring.from_text({
                'rndc-key.' : conf['key']
                })
        update = dns.update.Update(domain, keyring=keyring)
        update.present(svc)
        update.delete(svc, 'a')
        resp = dns.query.tcp(update, conf['ip'])
        dns_query_status(resp.rcode())

def dns_query_status(rcode):
    if rcode == 0:
        print('...Success')
    elif rcode == 6:
        print('...Alredy Exists')
    else:
        print('...Failed. RCode:', rcode)

if __name__ == "__main__":
    try:
        docker_int()
    except KeyboardInterrupt:
        pass
    finally:
        print('\nScript soft exit')
