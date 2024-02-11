#!/usr/bin/env python3

from io import BytesIO
from imdb import Movie
from PIL import Image
import subprocess
import requests
import clogger
import PTN
import os


class ImEdit:
    def __init__(self):
        self.log = clogger.log(os.getenv('LOG_LEVEL'), logger_name='Image')
        self.jfdb = os.getenv('JF_MOVIE_DIR')
        self.parser = PTN
        self.jf_movie_titles = self._jf_movies()

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

    def _image2bytes(self, image: list[bytes]) -> bytes:
        byte_array = BytesIO()
        image.save(byte_array, format='PNG')
        return byte_array.getvalue()

    def _download_bytes(self, url: str) -> list[bytes]:
        byte_array = requests.get(url).content
        return byte_array
    
    def _add_border(
            self, 
            url: str,
            thickness: int=8,
            color: str=(0, 255, 255)
        ) -> list[bytes]:
        byte_array = self._download_bytes(url)
        image = Image.open(BytesIO(byte_array))
        bordered_image = Image.new(
            "RGB", (
                image.width + 2 * thickness, 
                image.height + 2 * thickness
            ), color
        )
        bordered_image.paste(image, (thickness, thickness))
        return self._image2bytes(bordered_image)
    
    def isin_jellyfin(self, movie: Movie.Movie) -> bool:
        movie_title = movie[b'title'].lower()
        movie_title = movie_title.decode('utf-8')
        if movie_title in self.jf_movie_titles:
            self.log.debug(f' movie is in JFDB: {movie_title}')
            return True 
        else:
            self.log.debug(f'movie not in JFDB: {movie_title}')
            return False 

    def download_edit_cover(
            self, 
            movie: Movie.Movie, 
            border: int=5,
            color: str='pink'
        ) -> list[bytes]:
        try:
            image_url = movie['full-size cover url']
        except KeyError as e:
            self.log.warning(f'no movie url: {e}')
            return None
        else:
            movie_title = movie['title'].lower()
            if movie_title in self.jf_movie_titles:
                self.log.info(f' Is in JFDB: {movie_title}')
                return self._add_border(image_url)
            else:
                self.log.info(f'Not in JFDB: {movie_title}')
                return self._download_bytes(image_url)


