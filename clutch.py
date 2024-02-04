import pandas as pd
import requests
import clogger
import json
import PTN
import os
import __init__


class Clutch:
    host = os.getenv('TORRENT_API_HOST')
    port = os.getenv('TORRENT_API_PORT')
    path = os.getenv('TORRENT_API_PATH')

    def __init__(self):
        self.api_url = f'http://{self.host}:{self.port}/api/v1'
        self.log = clogger.log(os.getenv('LOG_LEVEL'), logger_name='clutch')
        self.log.propagate = False
        self.connect()

    def connect(self):
        try:
            requests.get(self.api_url)
        except Exception as error:
            import subprocess
            cmd = ['python', f'{self.path}/main.py']
            logfile = open('.logs/Spin.log', 'w')
            self.process = subprocess.Popen(
                cmd, stdout=logfile, stderr=subprocess.STDOUT
            )

    def _curl(self, url):
        resp = requests.get(url)
        resp = resp.content.decode('utf-8')
        return json.loads(resp)

    def _cover(self, entry):
        if isinstance(entry, str):
            return entry
        elif isinstance(entry, list):
            return entry[0]

    def _data2df(self, data, search_str):
        results = {
            'name': [], 'size': [], 'date': [],
            'seeders': [], 'leechers': [],
            'poster': [], 'magnet': [],
            'year': [], 'codec': [],
            'resolution': [], 
            'language': []
        }
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
                            retsults[key].append(None)
                    else:
                        results[key].append(str(info[key]))
                elif key in torrent.keys():
                    results[key].append(torrent[key])
                else:
                    if key == 'language':
                        results[key].append(None)
                    else:
                        results[key].append('NA')

        df = pd.DataFrame(results)
        df = df[df['name'].str.contains(search_str, case=False)]
        df = df[(df['codec'] != 'NA') | (df['resolution'] != 'NA')]
        return df

    def sites(self):
        url = f'{self.api_url}/sites'
        return self._curl(url)

    def query(self, movie, site='kickass'):
        self.log.info(f'query with {movie=}, {site=}')
        url = f'{self.api_url}/search?site={site}&query={movie}'
        data = self._curl(url)
        df =self._data2df(data=data, search_str=movie)
        return df

    def close(self):
        self.process.terminate()
        self.process.wait()

