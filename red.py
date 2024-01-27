from imdb import Movie
import clogger
import redis
import os
import __init__


class Database:
    """
    Redis Entertainment Database
    set and get movies from the redis database
    to be called by Movies class
    """
    expire_time = os.getenv('REDIS_EXPIRE_SECONDS')
    port = int(os.getenv('REDIS_PORT'))
    host = os.getenv('REDIS_IP_ADDR')
    infokeys = [
        'genres',
        'runtimes',
        'languages',
        'original air date',
        'imdbID',
        'videos',
        'title',
        'plot',
        'full-size cover url'
    ]

    def __init__(self, decode=True):
        self.log = clogger.log(level='INFO', logger_name='red')
        self.client = redis.Redis(
            host=self.host, port=self.port, decode_responses=decode
        )
        if not self.client.ping():
            raise ConnectionRefusedError(
                f'Could not connect to redis: {self.host}:{self.port}'
            )

    def _set_movie(self, genre: str, movie: Movie.Movie):
        movie_map = {}
        for info in self.infokeys:
            try:
                if isinstance(movie[info], str):
                    movie_map[info] = movie[info]
                elif isinstance(movie[info], list):
                    movie_map[info] = movie[info][0]
            except KeyError as error:
                self.log.warning(f'{error=}')
        self.client.hmset(
            name=f'{genre}:{movie.movieID}',
            mapping=movie_map
        )
    
    def set_movies_by_genre(self, genre: str, movies: list[Movie.Movie]):
        for movie in movies:
            self._set_movie(genre=genre, movie=movie)

    def _get_movie(self, name: str) -> dict:
        return self.client.hgetall(name=name)

    def get_movies_by_genre(self, genre: str) -> list[dict]:
        names = [name for name in self.client.scan_iter(match=f'{genre}*')]
        movies = []
        for name in names:
            movie = self._get_movie(name=name)
            movies.append(movie)
        return movies



