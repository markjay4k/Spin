from red import Database
import streamlit as st
import clogger


class Images:
    def __init__(self, columns):
        self.log = clogger.log('INFO', logger_name=__name__)
        self.db = Database()
        self.cover_key = 'full-size cover url'
        self.title_key = 'title'
        self.columns = columns

    def display_images_in_grid(self, genre):
        self.log.info(f'building image page for {genre} movies')
        st.title(f'{genre.upper()} MOVIES')
        for index, (movie, url) in enumerate(self._cover_urls(genre=genre)):
            if index % self.columns == 0: 
                cols = st.columns(self.columns, gap='small')
            with cols[index % self.columns]:
                st.image(
                    url, use_column_width=True, caption=movie[self.title_key]
                )
    
    def _cover_urls(self, genre):
        movies = self.db.get_movies_by_genre(genre=genre)
        for movie in movies:
            try:
                url = movie[self.cover_key]
            except KeyError as error:
                self.log.warning(f'{movie[self.title_key]}: {error}')
            else:
                yield (movie, url)


if __name__ == '__main__':
    Images(columns=6).display_images_in_grid('horror')
