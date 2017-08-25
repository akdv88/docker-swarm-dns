#### Simple Python3 script for updating dynamic domain zone with records, based on specified label of each currently running service in docker swarm mode.

### IMPORTANT: Must be run on swarm master nodes.

## Usage:
Requred options format:
* -s ipaddress,ipaddress,...
* -n "{'name1':{'ip':'ipaddress1','key':'key1'},'name2':{'ip':'ipaddress2','key':'key2'},...}"
* -d domainname.
* -u updatetime_in_seconds

### as standalone script on master node:
.swarm-ddns.py -s X -n X -d X -u X

### as standalone container:
docker run -d -v /var/run/docker.sock:/var/run/docker.sock akdv88/swarm-ddns -s X -n X -d X -u X

### as swarmmode service:
docker service create --constraint 'your_master_nodes label' --mount type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock akdv88/swarm-ddns -s X -n X -d X -u X
### as swarmmode stack
docker stack deploy -c /your-path/docker-compose.yml swarm-ddns
#### To enable DDNS update for your service just add label "add.dns=yourname" to it. To remove dns record either simply remove label from service or remove service itself.
