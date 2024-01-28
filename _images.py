from PIL import Image
from io import BytesIO
import subprocess
import requests
import clogger
import PTN


class Image:
    def __init__(self):
        self.log = clogger.log('INFO', logger_name='Image')
        self.jfdb = '/store/media/jellyfin/media/movies'
        self.parser = PTN
        self.jf_movie_titles = self._jf_movies()

    def _jf_movies(self) -> list[str]:
        command = ['ssh', 'mork', 'ls', self.jfdb]
        movies = subprocess.run(command, capture_output=True)
        movies = jfmovs.stdout.decode('utf-8').strip().split('\n')
        jf_movie_titles = []
        for movie in movies:
            try:
                title = self.parser.parse(movie)['title'].lower()
            except KeyError as error:
                self.log.debug(f'can\'t parse title: {movie}')
            else:
                jf_movie_titles.append(title)
        return jf_movie_titles

    def _download_image(self, url: str) -> list[bytes]:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        return image
    
    def _add_border(
            self, 
            url: str,
            thickness: int=5,
            color: str='pink'
        ) -> list[bytes]:
        image = self._download_image(url)
        bordered_image = Image.new(
            "RGB", (
                image.width + 2 * thickness, 
                image.height + 2 * thickness
            ), color
        )
        bordered_image.paste(image, (thickness, thickness))
        return bordered_image
    
    def download_edit_cover(self, movie, border=5, color='pink'):
        try:
            image_url = movie['full-size cover url'].decode('utf-8')
        except KeyError as e:
            return None
        else:
            movie_title = movie['title'].decode('utf-8').lower()
            if movie_title in self.jf_movie_titles:
                return self._bordered_image(image_url)
            else:
                return self._download_image(image_url)


