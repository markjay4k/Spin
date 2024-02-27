#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor
from imdb import IMDbDataAccessError
from requests import HTTPError
from imdb import Cinemagoer
from imdb import IMDbError
from red import Database
import clogger
import os
import __init__


class Movies:
    """use cinemagoer top50 search to get top40 movies by genre"""
    def __init__(self):
        self.log = clogger.log(level=os.getenv('LOG_LEVEL'))
        self.imdb_client = Cinemagoer()
        try:
            self.movie_db = Database()
        except ConnectionRefusedError as error:
            self.log.error(f'{error}')

    def _get_movie(self, movie_id: str) -> str:
        return self.imdb_client.get_movie(movie_id)

    def top40_by_genre(self, genre) -> None:
        top_movies = self.imdb_client.get_top50_movies_by_genres(genre)[:40]
        ids = (m.movieID for m in top_movies)
        if len(top_movies) % 20 == 0:
            workers = 20
        try:
            with ThreadPoolExecutor(max_workers=workers) as executor:
                movies = executor.map(self._get_movie, ids)
        except IMDbError as error:
            self.log.warning(f'IMDbError: {error=}')
        except HTTPError as error:
            self.log.warning(f'HTTPError: {error=}')
        except IMDbDataAccessError as error:
            self.log.warning(f'IMDbDataAccessError: {error=}')
        except TimeoutError as error:
            self.log.warning(f'TimeoutError: {error=}')
        else:
            self.movie_db.set_movies_by_genre(genre=genre, movies=movies)


