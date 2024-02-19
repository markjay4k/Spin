#!/usr/bin/env python3

from transmission_rpc import torrent
from transmission_rpc import Client
import clogger
import os


class Agent:
    """
    transmission bittorrent client API
    """
    host = os.getenv('TRANSMISSION_IP')
    port = os.getenv('TRANSMISSION_PORT')
    user = os.getenv('TRANSMISSION_USER')
    passwd = os.getenv('TRANSMISSION_PASS')

    def __init__(self):
        self.log = clogger.log(os.getenv('LOG_LEVEL'))
        self.agent = Client(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.passwd,
        )

    @property
    def torrents(self) -> list[torrent.Torrent]:
        return self.agent.get_torrents()

    def download(self, magnet: str) -> torrent.Torrent:
        torrent = self.agent.add_torrent(torrent=magnet)
        return torrent
