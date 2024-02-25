import requests
import json
import os
import PTN


def vpn_check(func):
    """VPN kill switch decorator"""
    def inner_function(*args, **kwargs):
        server_ip = requests.get('https://ipinfo.io').json()['ip']
        vpn_ip = os.getenv('VPN_IP') 
        if server_ip != vpn_ip:
            raise AttributeError('VPN IS DOWN')
        else:
            return func(*args, **kwargs)
    return inner_function

