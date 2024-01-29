from red import Database
import streamlit as st
import clogger
import os


class Images:
    def __init__(self, columns, urls=True):
        self.columns = columns
        self.urls = urls
        self.log = clogger.log(os.getenv('LOG_LEVEL'), logger_name=__name__)
        self.db = Database(decode=False)
        if self.urls:
            self.cover_key = b'full-size cover url'
            self.title_key = b'title'
        else:
            self.cover_key = b'cover_image'
            self.title_key = b'title'

    def _decode(self, key: str) -> str:
        return key.decode('utf-8') 

    def display_images_in_grid(self, genre):
        st.set_page_config(
            page_title=f'TOP40 MOVIES',
            initial_sidebar_state='auto',
            menu_items=None,
            page_icon=None,
            layout='wide', 
        )
        st.title(f'{genre.upper()} MOVIES')
        self.log.info(f'building image page for {genre} movies')
        for index, (movie, url) in enumerate(self._cover_urls(genre=genre)):
            if index % self.columns == 0: 
                cols = st.columns(self.columns, gap='small')
            with cols[index % self.columns]:
                st.image(
                    url, use_column_width=True,
                )
                _title = self._decode(movie[self.title_key])
                _year = self._decode(movie[b'original air date'])
                st.caption(
                    body=_title,
                    help=f"__{_title} ({_year})__\n\r{self._decode(movie[b'plot'])}"
                )
    
    def _cover_urls(self, genre):
        movies = self.db.get_movies_by_genre(genre=genre)
        for movie in movies:
            try:
                url = self._decode(movie[self.cover_key])
            except KeyError as error:
                self.log.warning(f'{self._decode(movie[self.title_key])}: {error}')
            else:
                yield (movie, url)


if __name__ == '__main__':
    Images(columns=6).display_images_in_grid('horror')
