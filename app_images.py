#!/usr/bin/env python3

from clutch import Clutch
from red import Database
import streamlit as st
import pandas as pd
import clogger
import time
import os


class Images:
    def __init__(self, columns, urls=True):
        self.columns = columns
        self.urls = urls
        self.log = clogger.log(os.getenv('LOG_LEVEL'), logger_name=__name__)
        self.log.propagate = False
        self.db = Database(decode=False)
        self.genres = self.db.genres
        if self.urls:
            self.cover_key = b'full-size cover url'
            self.title_key = b'title'
        else:
            self.cover_key = b'cover_image'
            self.title_key = b'title'

        self.tapi = Clutch()
        st.set_page_config(
            page_title=f'TOP40 MOVIES',
            initial_sidebar_state='auto',
            menu_items=None,
            page_icon=None,
            layout='wide', 
        )
        tabs = st.tabs(('__SEARCH__', *self.genres))
        genres = ('SEARCH', *self.genres)
        self.tabs = {
            genre: tab for genre, tab in zip(genres, tabs)
        }

    def _decode(self, key: str) -> str:
        return key.decode('utf-8') 

    def build_tabs(self):
        for genre, tab in self.tabs.items():
            with tab:
                if genre == 'SEARCH':
                    self.torrent_search()
                else:
                    self.display_images_in_grid(genre)
    
    def torrent_search(self):
        st.title('TORRENT-API SEARCH')
        col_text, col_button = st.columns([4, 1])
        with col_text:
            self.torrent_search = st.text_input(
                label='torrent search', value='', 
                help='search string for torrent-API'
            )
        with col_button:
            self.button = st.button(
                'search', key='search', 
                help='search for torrent with torrent-API',
                use_container_width=False,
            )
        if self.button:
            df = self.tapi.query(self.torrent_search)
            df_col = st.columns(1)
            with df_col[0]:
                st.dataframe(
                    data=df, 
                    column_config={
                        'name': st.column_config.TextColumn(
                            'name', disabled=True
                        ), 
                        'date': st.column_config.TextColumn(
                            'release', max_chars=4, disabled=True
                        ),
                        'genre': st.column_config.ListColumn(
                            'genres', width='medium'
                        ),
                        'rating': st.column_config.TextColumn(
                            'rating', disabled=True
                        ),
                        'poster':  st.column_config.ImageColumn(
                            label='poster', width='small'
                        ),
                        'size': st.column_config.TextColumn(
                            'size', disabled=True
                        ),
                        'magnet': st.column_config.TextColumn(
                            'magnet', disabled=True
                        )
                    },
                    use_container_width=True,
                    hide_index=True
                )

    def display_images_in_grid(self, genre):
        st.header(f'{genre.upper()} MOVIES')
        self.log.info(f'building image page for {genre} movies')
        for index, (movie, url) in enumerate(self._cover_urls(genre=genre)):
            if index % self.columns == 0: 
                cols = st.columns(self.columns, gap='small')
            with cols[index % self.columns]:
                st.image(url, use_column_width=True)
                _title = self._decode(movie[self.title_key])
                _year = self._decode(movie[b'original air date'])
                _plot = self._decode(movie[b'plot']) 
                st.caption(
                    body=_title,
                    help=f"__{_title} ({_year})__\n\r{_plot}"
                )
    
    def _cover_urls(self, genre):
        movies = self.db.get_movies_by_genre(genre=genre)
        for movie in movies:
            try:
                url = self._decode(movie[self.cover_key])
            except KeyError as error:
                title = self._decode(movie[self.title_key])
                self.log.debug(f'{title}: missing: {(error)}')
            else:
                yield (movie, url)


if __name__ == '__main__':
    Images(columns=6).build_tabs()

