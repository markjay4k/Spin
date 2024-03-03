#!/usr/bin/env python3

from transmission_rpc import Client
from imdb import Movie
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
        self.sshkey_path = os.getenv('TRANSMISSION_SSHKEY_FILEPATH')
        self.jfdb = os.getenv('JF_MOVIE_DIR')
        self.agent = Client(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.passwd,
        )
        self.movies = self.all_movies()

    def all_movies(self):
        jfmovies = self._jf_movies()
        trmovies = self._torrents()
        all_movies = [*jfmovies, *trmovies]
        return all_movies

    def _jf_movies(self) -> list[str]:
        command = [
            'ssh', '-o', 'StrictHostKeyChecking=accept-new',
            f'mark@{self.host}', '-i', self.sshkey_path,
            'ls', self.jfdb
        ]
        command = ['ssh', 'mork', 'ls', self.jfdb]
        movies = subprocess.run(command, capture_output=True)
        movies = movies.stdout.decode('utf-8').strip().split('\n')
        jf_movie_titles = []
        for movie in movies:
            try:
                title = PTN.parse(movie)['title'].lower()
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
                torrs.append(info['title'].lower())
        return torrs 

    def isin_jellyfin(self, movie: Movie.Movie) -> bool:
        movie_title = movie[b'title'].lower()
        movie_title = movie_title.decode('utf-8')
        if movie_title in self.movies:
            self.log.debug(f' movie is in JFDB: {movie_title}')
            return True 
        else:
            self.log.debug(f'movie not in JFDB: {movie_title}')
            return False 


