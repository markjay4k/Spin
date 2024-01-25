from imdb import Movie
import clogger
import redis
import os
import __init__


class Database:
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

    def __init__(self):
        self.log = clogger.log(level='INFO', logger_name='red')
        self.client = redis.Redis(
            host=self.host, port=self.port, decode_responses=True
        )
        if not self.client.ping():
            raise ConnectionRefusedError(
                f'Could not connect to redis: {self.host}:{self.port}'
            )

    def set_movie(self, genre: str, movie: Movie.Movie):
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
            self.set_movie(genre=genre, movie=movie)

    def get_movie(self, name: str) -> dict:
        return self.client.hgetall(name=name)

    def get_movies_by_genre(self, genre: str) -> list[dict]:
        names = [name for name in self.client.scan_iter(match=f'{genre}*')]
        movies = []
        for name in names:
            movie = self.get_movie(name=name)
            movies.append(movie)
        return movies



