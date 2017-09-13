
<p align="center">
<img src="https://www.tuleap.org/sites/default/files/docker-swarm.jpg" alt="swarm" title="swarm" />
</p>

[![](https://images.microbadger.com/badges/version/akdv88/swarm-ddns.svg)](https://microbadger.com/images/akdv88/swarm-ddns "Get your own version badge on microbadger.com")
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/containous/traefik/blob/master/LICENSE.md)

#### Simple Python3 script for updating dynamic domain zone with records, based on specified label of each currently running service in docker swarm mode.

### IMPORTANT: Must be run on swarm master nodes.

## Usage:
Requred options format:
* -s ipaddress,ipaddress,...
* -n "{'name1':{'ip':'ipaddress1','key':'key1'},'name2':{'ip':'ipaddress2','key':'key2'},...}"
* -d domainname.

### as standalone script on master node:
.swarm-ddns.py -s X -n X -d X 

### as standalone container:
docker run -d -v /var/run/docker.sock:/var/run/docker.sock akdv88/swarm-ddns -s X -n X -d X

### as swarmmode service:
docker service create --constraint 'your_master_nodes label' --mount type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock akdv88/swarm-ddns -s X -n X -d X
### as swarmmode stack
docker stack deploy -c /your-path/docker-compose.yml swarm-ddns
#### To enable DDNS update for your service just add label "add.dns=yourname" to it. To remove dns record either simply remove label from service or remove service itself.
