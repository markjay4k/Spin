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
        results = {
            'title': [],
            'name': [], 'size': [],
            'date': [], 'category': [],
            'seeders': [], 'leechers': [],
            'magnet': [], 'year': [],
            'codec': [], 'resolution': []
        }
        for torr in data['data']:
            info = PTN.parse(torr['name'])
            for key in results.keys():
                if key in torr.keys():
                    results[key].append(torr[key])
                elif key in info.keys():
                    results[key].append(info[key])
                else:
                    results[key].append('NA')
        df = pd.DataFrame(results)
        df['seeders'] = df['seeders'].astype('uint16')
        df['leechers'] = df['leechers'].astype('uint16')
        df = df[df['name'].str.contains(search_str, case=False)]
        df = df[df['magnet'] != 'NA']
        df = df.loc[(~df['name'].str.contains('XXX', case=True))]
        return df

    def _kickass2df(self, data: dict, search_str: str) -> pd.DataFrame:
        results = {
            'name': [], 'size': [], 'date': [],
            'seeders': [], 'leechers': [],
            'poster': [], 'magnet': [],
            'year': [], 'codec': [],
            'resolution': [], 
            'language': []
        }
        if 'data' not in data.keys():
            return pd.DataFrame(results)

        for torrent in data['data']:
            info = PTN.parse(torrent['name'])
            for key in results:
                if key == 'poster':
                    if key in torrent.keys():
                        poster = self._cover(torrent[key])
                    elif 'screenshot' in torrent.keys():
                        poster = self._cover(torrent['screenshot'])
                    else:
                        poster = 'NA'
                    results[key].append(poster)
                elif key in info.keys():
                    if key == 'language':
                        if isinstance(info[key], list):
                            results[key].append(info[key])
                        elif isinstance(info[key], str):
                            results[key].append([info[key]])
                        else:
                            results[key].append(None)
                    else:
                        try:
                            value = int(info[key])
                        except ValueError as error:
                            value = info[key]
                        finally:
                            results[key].append(value)
                elif key in torrent.keys():
                    if key in ('seeders', 'leechers'):
                        try:
                            value = int(torrent[key])
                        except ValueError as error:
                            value = np.nan
                        finally:
                            results[key].append(value)
                    else:
                        results[key].append(torrent[key])
                else:
                    if key == 'language':
                        results[key].append(None)
                    else:
                        results[key].append(None)

        df = pd.DataFrame(results)
        df['seeders'] = df['seeders'].astype('uint16')
        df['leechers'] = df['leechers'].astype('uint16')
        df = df[df['name'].str.contains(search_str, case=False)]
        df = df[(df['codec'] != 'NA') & (df['resolution'] != 'NA')]
        df = df.loc[(~df['name'].str.contains('XXX', case=True))]
        return df

    def sites(self):
        url = f'{self.api_url}/sites'
        return self._curl(url)

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
            df = pd.DataFrame(
                results = {
                    'title': [],
                    'name': [], 'size': [],
                    'date': [], 'category': [],
                    'seeders': [], 'leechers': [],
                    'magnet': [], 'year': [],
                    'codec': [], 'resolution': []
                }
            )
        return df

    def close(self):
        self.process.terminate()
        self.process.wait()

