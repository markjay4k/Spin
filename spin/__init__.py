#!/usr/bin/env python3

import subprocess
import clogger
import json
import os


class start_redis:
    def __init__(self):
        self.log = clogger.log('INFO', logger_name='init')
        if not self.is_running_in_docker():
            self.envs()

    def is_running_in_docker(self):
        if os.path.exists('/.dockerenv'):
            os.environ['WORKDIR'] = '/app'
            return True
        try:
            with open('/proc/1/cgroup', 'rt') as f:
                if 'docker' in f.read():
                    os.environ['WORKDIR'] = '/app'
                    return True
        except FileNotFoundError as error:
            self.log.warning(f'{error}')
            os.environ['WORKDIR'] = '.'
            return False

    def docker_network(self, name):
        network_info = subprocess.run(
            ['docker', 'network', 'inspect', f'{name}'], capture_output=True
        )
        network_info = json.loads(network_info.stdout).pop()
        for k, v in network_info['Containers'].items():
            address, netsize = v['IPv4Address'].split('/')
            self.log.debug(f'IPv4Address: {address}')
            #break
        return address
    
    def envs(self):
        envs = {}
        with open('.env', 'r') as file:
            for line in file.readlines():
                if line.strip() == '':
                    continue
            
                var, value = line.strip().split('=')
                #if var == 'REDIS_IP_ADDR':
                #    value = self.docker_network(value)

                self.log.debug(f'{var}: {value}')
                os.environ[var] = value
                envs[var] = value


start_redis()
