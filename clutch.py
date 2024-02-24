#!/usr/bin/env python3

import pandas as pd
import numpy as np
import requests
import clogger
import json
import PTN
import os
import __init__


class Clutch:
    """API for torrent-API-py"""
    host = os.getenv('TORRENT_API_HOST')
    port = os.getenv('TORRENT_API_PORT')
    path = os.getenv('TORRENT_API_PATH')

    categories = ['name', 'size', 'seeders', 'magnet', 'date']
    goodsites = [
        'torrentproject',
        'limetorrent',
        'piratebay',
        'bitsearch',
        'magnetdl',
        'kickass',
        'torlock',
        'nyaasi',
    ]

    def __init__(self) -> None:
        self.api_url = f'http://{self.host}:{self.port}/api/v1'
        self.log = clogger.log(os.getenv('LOG_LEVEL'))
        self.log.propagate = False
        self.connect()
        self.results = {
            'title': [],
            'name': [], 'size': [],
            'date': [], 'category': [],
            'seeders': [], 'leechers': [],
            'magnet': [], 'year': [],
            'codec': [], 'resolution': []
        }

    def connect(self) -> None:
        try:
            requests.get(self.api_url)
        except Exception as error:
            import subprocess
            cmd = ['python', f'{self.path}/main.py']
            logfile = open('.logs/Spin.log', 'w')
            self.process = subprocess.Popen(
                cmd, stdout=logfile, stderr=subprocess.STDOUT
            )

    def sites(self):
        url = f'{self.api_url}/sites'
        return self._curl(url)

    def _curl(self, url: str) -> dict:
        resp = requests.get(url)
        resp = resp.content.decode('utf-8')
        return json.loads(resp)

    def _cover(self, entry):
        if isinstance(entry, str):
            return entry
        elif isinstance(entry, list):
            n_pics = len(entry) // 2
            return entry[n_pics]

    def _lime2df(self, data: dict, search_str: str) -> pd.DataFrame:
        results = self.results.copy()
        for torr in data['data']:
            info = PTN.parse()
            for key in results.keys():
                if key in torr.keys():
                    results[key].append(torr[key])
                elif key in info.keys():
                    results[key].append(info[key])
                else:
                    results[key].append('NA')
        df = pd.DataFrame(results)
        df = self._clean_df(df, search_str)
        return df

    def _clean_df(self, df, search_str):
        try:
            df['seeders'] = df['seeders'].astype('uint16')
            df['leechers'] = df['leechers'].astype('uint16')
        except ValueError as error:
            df['seeders'] = df['seeders'].map(self._replace).astype('uint16')
            df['leechers'] = df['leechers'].map(self._replace).astype('uint16')
            self.log.warning(f'{error}')

        df = df[df['name'].str.contains(search_str, case=False)]
        df = df[df['magnet'] != 'NA']
        df = df.loc[(~df['name'].str.contains('XXX', case=True))]
        return df

    def _replace(self, seed):
        return seed.replace(',', '')

    def _q2(self, movie, site='kickass'): 
        self.log.info(f'query with {movie=}, {site=}')
        url = f'{self.api_url}/search?site={site}&query={movie}'
        data = self._curl(url)
        return data 

    def query(self, movie, site='limetorrent'): 
        self.log.info(f'query: {movie=}, {site=}')
        url = f'{self.api_url}/search?site={site}&query={movie}'
        data = self._curl(url)
        if site == 'limetorrent':
            df = self._lime2df(data=data, search_str=movie)
        elif site == 'kickass':
            df = self._kickass2df(data=data, search_str=movie)
        else:
            self.log.warning(f'{site=} not supported')
            df = pd.DataFrame(self.results.copy())
        return df

    def close(self):
        self.process.terminate()
        self.process.wait()

