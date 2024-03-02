#!/usr/bin/env python3

import subprocess
import requests
import clogger
import os
import __init__


log = clogger.log(os.getenv('LOG_LEVEL'))
tr_host = os.getenv('TRANSMISSION_IP')

def local(func):
    def inner_function(*args, **kwargs):
        server_ip = requests.get('https://ipinfo.io/ip').text
        vpn_ip = os.getenv('VPN_IP') 
        if server_ip != vpn_ip:
            raise AttributeError('VPN IS DOWN')
        else:
            return func(*args, **kwargs)
    return inner_function


def remote(func):
    def inner_function(*args, **kwargs):
        command = [
            'ssh', '-o', 'StrictHostKeyChecking=accept-new',
            f'mark@{tr_host}', '-i', '/app/ssh/id_rsa',
            'curl', 'http://ipinfo.io/ip'
        ]
        try:
            responses = subprocess.run(command, capture_output=True)
            server_ip = responses.stdout.decode('utf-8')
            stderr = responses.stderr.decode('utf-8')
        except Exception as error:
            log.warning(f'could not check VPN: {error=}')
            log.warning(f'{server_ip=}')
            log.warning(f'{stderr=}')
            return False
        else:
            log.info(f'{server_ip=}')
            vpn_ip = os.getenv('VPN_IP') 
            if server_ip != vpn_ip:
                raise AttributeError('VPN IS DOWN')
            else:
                return func(*args, **kwargs)
    return inner_function
