from imdb import Cinemagoer
import pandas as pd
from rdf import Rdf
import time


class Movies:
    def __init__(self):
        self.redis_key = 'top50_movies_by_genres'
        self.imdb_client = Cinemagoer()
        self.categories = [
            'action',
            'comedy',
            'crime',
            'drama',
            'family',
            'fantasy',
            'horror',
            'sci-fi',
            'thriller'
        ]

    def _to_df(self, movies, category):
        df_list = []
        for movie in movies:
            movie_dict = {key: value for key, value in movie.items()}
            movie_dict['_search_category'] = category
            df_list.append(pd.Series(movie_dict))
        return Rdf(pd.concat(df_list))

    def _search_imdb(self):
        results_by_genre = []
        for category in self.categories:
            movies = self.imdb_client.get_top50_movies_by_genres(category)
            results_by_genre.append(self._to_df(movies, category))
            time.sleep(0.01)
        return Rdf(pd.concat(results_by_genre))

    def top50_movies(self):
        try:
            top50_df = Rdf.from_redis(self.redis_key)
        except Exception as e:
            top50_df = self._search_imdb()
            top50_df.to_redis(self.redis_key)
        finally:
            return top50_df
