from concurrent.futures import ThreadPoolExecutor
from imdb import Cinemagoer
from rdf import Rdf
import pandas as pd
import threading


class Movies:
    def __init__(self, genre):
        self.db_key = f'top_movies_{genre}'
        self.imdb_client = Cinemagoer()
        movies = self.imdb_client.get_top50_movies_by_genres(genre)
        self.workers = len(movies)
        self.ids = (m.movieID for m in movies)

    def _get_movie(self, movie_id: str):
        return self.imdb_client.get_movie(movie_id)

    def _search(self):
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            results = executor.map(self._get_movie, self.ids)
        df = pd.DataFrame({self.db_key: [r for r in results]})
        Rdf(df).to_redis(self.db_key)


if __name__ == '__main__':
    import time
    
    starttime = time.time()
    results = Movies('horror')._search()
    for result in results:
        print(result)
    print(f'duration: {time.time() - starttime:.2f}s')

