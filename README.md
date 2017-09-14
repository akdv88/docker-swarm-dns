
<p align="center">
<img src="https://www.tuleap.org/sites/default/files/docker-swarm.jpg" alt="swarm" title="swarm" />
</p>

[![](https://images.microbadger.com/badges/version/akdv88/swarm-ddns.svg)](https://microbadger.com/images/akdv88/swarm-ddns "Get your own version badge on microbadger.com")
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/containous/traefik/blob/master/LICENSE.md)

#### Simple Python3 script for updating dynamic domain zone with records, based on specified label of each currently running service in docker swarm mode.

#### How it works:
When script initializes for the first time, it retrieves a list of running services with "add.dns" label and then sends DNS Update to your DDNServer based on those labels. After that it starts to listen docker socket for events and all the next updates to DDNS will be performed automatically:
* creating/removing service with defined "add.dns" label
* adding/updating/removing "add.dns" label in service

#### IMPORTANT: Must be run on swarm master nodes in replicated mode (with at least two replicas). This is necessary, because some events are strangely distributed among master nodes - some of them are completely invisible on the leader node.
## Usage:

Requred options format:
* -s ipaddress,ipaddress,...
* -n "{'name1':{'ip':'ipaddress1','key':'key1'},'name2':{'ip':'ipaddress2','key':'key2'},...}"
* -d domainname.

### You can run it as a standalone script on master node
.swarm-ddns.py -s X -n X -d X 

### Or as a standalone container
docker run -d -v /var/run/docker.sock:/var/run/docker.sock akdv88/swarm-ddns -s X -n X -d X

### As a swarmmode service
docker service create --constraint 'your_master_nodes label' --mount type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock akdv88/swarm-ddns -s X -n X -d X
### And even as aswarmmode stack
docker stack deploy -c /your-path/docker-compose.yml swarm-ddns
#### To enable DDNS update for your service just add label "add.dns=yourname" to it. To remove dns record either simply remove label from service or remove service itself.
