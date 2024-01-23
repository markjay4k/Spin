import subprocess
import json
import os


def docker_network(name):
    """get the redis-db docker IP address"""

    network_info = subprocess.run(
        ['docker', 'network', 'inspect', name], capture_output=True
    )
    network_info = json.loads(network_info.stdout).pop()
    for k, v in network_info['Containers'].items():
        address, netsize = v['IPv4Address'].split('/')
    return address


def envs():
    """convert .envs to environment variables"""

    envs = {}
    with open('.env', 'r') as file:
        for line in file.readlines():
            var, value = line.strip().split('=')
            os.environ[var] = value
            envs[var] = value
            if 'NETWORK' in var:
                address = docker_network(value)
                os.environ['REDIS_IP_ADDR'] = address
                envs['REDIS_IP_ADDR'] = address


envs()
