#!/usr/bin/env python3

from transmission_rpc import Client
import subprocess
import clogger
import PTN
import os
import __init__


class JFDB:
    host = os.getenv('TRANSMISSION_IP')
    port = os.getenv('TRANSMISSION_PORT')
    user = os.getenv('TRANSMISSION_USER')
    passwd = os.getenv('TRANSMISSION_PASS')

    def __init__(self):
        self.log = clogger.log(os.getenv('LOG_LEVEL'))
        self.log.info('checking')
        self.jfdb = os.getenv('JF_MOVIE_DIR')
        self.parser = PTN
        self.jf_movie_titles = self._jf_movies()
        self.agent = Client(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.passwd,
        )

    def movies(self):
        jfmovies = self._jf_movies()
        trmovies = self._torrents()
        all_movies = [*jfmovies, *trmovies]
        return all_movies

    def _jf_movies(self) -> list[str]:
        command = ['ssh', 'mork', 'ls', self.jfdb]
        movies = subprocess.run(command, capture_output=True)
        movies = movies.stdout.decode('utf-8').strip().split('\n')
        jf_movie_titles = []
        for movie in movies:
            try:
                title = self.parser.parse(movie)['title'].lower()
            except KeyError as error:
                self.log.debug(f'can\'t parse title: {movie}')
            else:
                jf_movie_titles.append(title)
        return jf_movie_titles

    def _torrents(self) -> list[str]:
        torrents = self.agent.get_torrents()
        torrs = []
        for torr in torrents:
            info = PTN.parse(torr.name)
            if 'title' in info.keys():
                torrs.append(info['title'])
        return torrs 

