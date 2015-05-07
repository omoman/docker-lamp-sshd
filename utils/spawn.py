#!/usr/bin/env python

"""
USAGE:
	spawn.py <# of containers> <first http port> <first ssh port>

EXAMPLE:
	spawn.py 30 8080 2222

RESULT:
	Script will create 30 containers running 'supervisord' using image docker.io/omoman/supervisord-lamp-sshd. 
	Each container will have their default HTTP (80) and SSH (22) forwarded 
	to an address starting from 8080 to 9010 (for HTTP) and 2222 to 2252 (for SSH). This script will also
	create a subdomain for each container, and add a vhost file for it automatically.
	Port collisions will break this script.

ARTIFACTS:
	A file 'containers.json' in the following format:
		{
			"<container_id_1>" :
			{
				ssh_port: <Number>,
				http_port: <Number>,
				subdomain_name: <String>
			},
			"<container_id_2>" :
			{
				ssh_port: <Number>,
				http_port: <Number>,
				subdomain_name: <String>
			},
			...
		}
"""

import json
import shlex
import sys
import subprocess

import haiku

vhost = """
<VirtualHost *:80>
    ServerName {subdomain}.acm-workshop.party
    ProxyPreserveHost On
    ProxyRequests Off   
    ProxyPass / http://localhost:{http_port}/
    ProxyPassReverse / http://localhost:{http_port}/
</VirtualHost>
"""

vhost_fname = "/etc/httpd/conf.d/000-{subdomain}.acm-workshop.party.conf"

def create_container(http_port, ssh_port):
	args = shlex.split('docker run -p {}:80 -p {}:22 -itd docker.io/omoman/supervisord-lamp-sshd supervisord'
							.format(http_port, ssh_port))
	container_id = subprocess.check_output(args)
	
	subdomain_name = haiku.haiku()
	subdomain_vhost_fname = vhost_fname.format(subdomain=subdomain_name)
	subdomain_vhost_contents = vhost.format(subdomain=subdomain_name, http_port=http_port)	

	with open(subdomain_vhost_fname, 'w') as f:
		f.write(subdomain_vhost_contents)

	return (container_id.strip(), subdomain_name)

if __name__ == "__main__":
	num_containers = int(sys.argv[1])
	start_http_port = int(sys.argv[2])
	start_ssh_port = int(sys.argv[3])
	containers = {}

	for (i, j) in zip(xrange(start_http_port, start_http_port + num_containers),
					xrange(start_ssh_port, start_ssh_port + num_containers)):
		container_id, subdomain = create_container(i, j)
		containers[container_id] = {"http_port":i, "ssh_port":j, "subdomain":subdomain}

	with open('containers.json', 'w') as f:
		f.write(json.dumps(containers))
		