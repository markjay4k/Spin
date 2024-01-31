import requests
import clogger
import json
import __init__
import os


class Clutch:
    host = os.getenv('TORRENT_API_HOST')
    port = os.getenv('TORRENT_API_PORT')
    path = os.getenv('TORRENT_API_PATH')

    def __init__(self):
        self.api_url = f'http://{self.host}:{self.port}/api/v1'
        self.log = clogger.log(os.getenv('LOG_LEVEL'), logger_name='clutch')
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

    def sites(self):
        url = f'{self.api_url}/sites'
        return self._curl(url)

    def query(self, movie, site='yts'):
        url = f'{self.api_url}/search?site={site}&query={movie}'
        return self._curl(url)

    def close(self):
        self.process.terminate()
        self.process.wait()

