from concurrent.futures import ThreadPoolExecutor
from imdb import IMDbDataAccessError
from requests import HTTPError
from imdb import Cinemagoer
from red import Database
import clogger
import __init__


class Movies:
    def __init__(self):
        self.imdb_client = Cinemagoer()
        self.movie_db = Database()
        self.log = clogger.log(level='INFO', logger_name='movies')

    def _get_movie(self, movie_id: str):
        return self.imdb_client.get_movie(movie_id)

    def top50_by_genre(self, genre):
        top_movies = self.imdb_client.get_top50_movies_by_genres(genre)[:40]
        ids = (m.movieID for m in top_movies)
        if len(top_movies) % 10 == 0:
            workers = 10

        try:
            with ThreadPoolExecutor(max_workers=workers) as executor:
                movies = executor.map(self._get_movie, ids)
        except HTTPError as error:
            self.log.warning(f'{error=}')
        except IMDbDataAccessError as error:
            self.log.exception(f'{error=}')
        else:
            self.movie_db.set_movies_by_genre(genre=genre, movies=movies)
