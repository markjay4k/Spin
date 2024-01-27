import subprocess
import clogger
import json
import os


class start_redis:
    def __init__(self):
        self.log = clogger.log('INFO', logger_name='init')
        self.check_status_and_start_redis()
        self.envs()

    def check_status_and_start_redis(self):
        inspect = [
            'docker', 'inspect', "--format='{{.State.Status}}'", 'redpanda'
        ]
        status = subprocess.run(inspect, capture_output=True)
        status = status.stdout.decode('utf-8').strip().replace('\'', '')
        if status == 'running':
            self.log.info(f'Redis is {status}')
        else:
            self.log.info(f'Redis is down. starting container')
            start = subprocess.run(
                ['docker', 'compose', 'up', '-d'],
                capture_output=True
            )
            start = start.stdout.decode('utf-8')
            self.log.info(f'{start}')
    
    def docker_network(self, name):
        network_info = subprocess.run(
            ['docker', 'network', 'inspect', f'{name}'], capture_output=True
        )
        network_info = json.loads(network_info.stdout).pop()
        for k, v in network_info['Containers'].items():
            address, netsize = v['IPv4Address'].split('/')
            self.log.debug(f'IPv4Address: {address}')
        return address
    
    def envs(self):
        envs = {}
        with open('.env', 'r') as file:
            for line in file.readlines():
                var, value = line.strip().split('=')
                self.log.debug(f'{var}: {value}')
                os.environ[var] = value
                envs[var] = value
                if 'NETWORK' in var:
                    address = self.docker_network(value)
                    os.environ['REDIS_IP_ADDR'] = address
                    envs['REDIS_IP_ADDR'] = address


start_redis()
