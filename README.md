[![](https://images.microbadger.com/badges/image/akdv88/swarm-ddns.svg)](https://microbadger.com/images/akdv88/swarm-ddns "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/version/akdv88/swarm-ddns.svg)](https://microbadger.com/images/akdv88/swarm-ddns "Get your own version badge on microbadger.com")
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/akdv88/swarm-ddns/blob/master/LICENSE.md)

#### Dockerised Python3 script for updating dynamic domain zone with records, based on specified label of each currently running service in docker swarm mode.

#### How it works:
#### If you want your service to be available by DNS, just add "add.dns=your_name" label to it.
When script will initialize for the first time, it'll retreive a list of running services with "add.dns" label and then will send DNS Update to your DynDNServer* based on those labels. After that it'll start to listen docker socket for events and all the next updates to DDNS will be performed automatically:
* creating/removing service with defined "add.dns" label
* adding/updating/removing "add.dns" label in service

#### IMPORTANT: Must be run on swarm master nodes in replicated mode (with at least two replicas). This is necessary, because some events are strangely distributed among master nodes - some of them are completely invisible on the leader node.

## Usage:

Requred options format:
* -s swarmnode1_ipaddress,swarmnode2_ipaddress,...
* -n "{'ddns1_name':{'ip':'ddns1_ipaddress','key':'ddns1_key'},'ddns2_name':{'ip':'ddns2_ipaddress','key':'ddns2_key'},...}"
* -d your_domainname.

### You can run it as a standalone Docker container
```
$ docker run -d -v /var/run/docker.sock:/var/run/docker.sock akdv88/swarm-ddns -s X -n X -d X
```
### Or as a Docker Swarm Mode service
```
$ docker service create --constraint 'node.role==manager' --mount type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock akdv88/swarm-ddns -s X -n X -d X
```
### And even as a Docker Swarm Mode stack
```
$ docker stack deploy -c /your-path/docker-compose.yml swarm-ddns
```
###### * Tested with Bind9 and NSD DNS servers
