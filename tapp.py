#!/usr/bin/env python3

from clutch import Clutch
from red import Database
import streamlit as st
import pandas as pd
import clogger
import time
import os


log = clogger.log(os.getenv('LOG_LEVEL'), logger_name=__name__)
log.propagate = False
db = Database(decode=False)
genres = db.genres
cover_key = b'full-size cover url'
title_key = b'title'
tapi = Clutch()
st.set_page_config(
    page_title=f'TOP40 MOVIES',
    initial_sidebar_state='auto',
    menu_items=None,
    page_icon=None,
    layout='wide', 
)
tabs = st.tabs(('__SEARCH__', *genres))
genres = ('SEARCH', *genres)
tabs = {genre: tab for genre, tab in zip(genres, tabs)}


def _decode(key: str) -> str:
    return key.decode('utf-8') 


def build_tabs(columns):
    for genre, tab in tabs.items():
        with tab:
            if genre == 'SEARCH':
                torrent_query()
            else:
                display_images_in_grid(genre, columns)


def torrent_query():
    st.title('TORRENT-API SEARCH')
    col_text, col_button = st.columns([4, 1])
    with col_text:
        torrent_search = st.text_input(
            label='torrent search', value='', 
            help='search string for torrent-API'
        )
    with col_button:
        button = st.button(
            'search', key='search', 
            help='search for torrent with torrent-API',
            use_container_width=False,
        )
    if button:
        df = tapi.query(torrent_search)
        df_col = st.columns(1)
        with df_col[0]:
            st.dataframe(
                data=df, 
                column_order=[
                    'name', 'year', 'size', 'seeders', 'leechers',
                    'codec', 'resolution', 'date', 
                    'poster', 'language', 'magnet'
                ]
                column_config={
                    'name': st.column_config.TextColumn(
                        'name', disabled=True
                    ), 
                    'size': st.column_config.TextColumn(
                        'size', disabled=True
                    ),
                    'date': st.column_config.TextColumn(
                        'uploaded', disabled=True
                    ),
                    'seeders': st.column_config.TextColumn(
                        'seeders', disabled=True
                    ),
                    'leechers': st.column_config.TextColumn(
                        'leechers', disabled=True
                    ),
                    'poster':  st.column_config.ImageColumn(
                        label='poster', width='small'
                    ),
                    'magnet': st.column_config.TextColumn(
                        'magnet', disabled=True
                    ),
                    'year': st.column_config.TextColumn(
                        'year', disabled=True
                    ),
                    'codec': st.column_config.TextColumn(
                        'codec', disabled=True
                    ),
                    'resolution': st.column_config.TextColumn(
                        'resolution', disabled=True
                    ),
                    'language': st.column_config.ListColumn(
                        'languages', width='medium'
                    ),
                },
                use_container_width=True,
                hide_index=True
            )


@st.cache_data
def display_images_in_grid(genre, columns):
    st.header(f'{genre.upper()} MOVIES')
    log.info(f'building image page for {genre} movies')
    for index, (movie, url) in enumerate(_cover_urls(genre=genre)):
        if index % columns == 0: 
            cols = st.columns(columns, gap='small')
        with cols[index % columns]:
            st.image(url, use_column_width=True)
            _title = _decode(movie[title_key])
            _year = _decode(movie[b'original air date'])
            _plot = _decode(movie[b'plot']) 
            st.caption(
                body=_title,
                help=f"__{_title} ({_year})__\n\r{_plot}"
            )


def _cover_urls(genre):
    movies = db.get_movies_by_genre(genre=genre)
    for movie in movies:
        try:
            url = _decode(movie[cover_key])
        except KeyError as error:
            title = _decode(movie[title_key])
            log.debug(f'{title}: missing: {(error)}')
        else:
            yield (movie, url)


if __name__ == '__main__':
    build_tabs(columns=6)

