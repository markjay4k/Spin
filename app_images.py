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
                on_click=self.tapi.query, args=(self.torrent_search, 'yts')
            )
            if self.button:
                self.data = self.tapi.data
                self.log.info(f'{data.keys()=}')

    def display_images_in_grid(self, genre):
        st.header(f'{genre.upper()} MOVIES')
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
    Images(columns=6).build_tabs()

