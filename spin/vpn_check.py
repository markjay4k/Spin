#!/usr/bin/env python3

import subprocess
import requests
import clogger
import os
import __init__


log = clogger.log(os.getenv('LOG_LEVEL'))

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
        command = ['ssh', 'mork', 'curl', 'http://ipinfo.io/ip']
        server_ip = subprocess.run(command, capture_output=True)
        server_ip = server_ip.stdout.decode('utf-8')
        log.info(f'{server_ip=}')
        vpn_ip = os.getenv('VPN_IP') 
        if server_ip != vpn_ip:
            raise AttributeError('VPN IS DOWN')
        else:
            return func(*args, **kwargs)
    return inner_function
