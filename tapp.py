#!/usr/bin/env python3

from clutch import Clutch
from red import Database
import streamlit as st
import pandas as pd
import clogger
import time
import os


def _decode(key: bytes) -> str:
    return key.decode('utf-8') 


def _togb(size: str) -> float:
    pf = (('KB', ''), ('MB', '1e3'), ('GB', 'e6'), (' ', ''))
    for switch in pf:
        size = size.replace(*switch)
    size = float(size) / 1e6
    return size


def search_cb(search_str, search_col):
    if search_str == '':
        return
    column_config={
        'name': st.column_config.TextColumn('name', disabled=True), 
        'size': st.column_config.NumberColumn('size (GB)', format='%.1f', disabled=True),
        'date': st.column_config.TextColumn('uploaded', disabled=True),
        'seeders': st.column_config.NumberColumn('seeders', disabled=True),
        'leechers': st.column_config.NumberColumn('leechers', disabled=True),
        'poster':  st.column_config.ImageColumn('poster', width='small'),
        'year': st.column_config.NumberColumn('year', format="%4d", disabled=True),
        'resolution': st.column_config.TextColumn('resolution', disabled=True),
        'language': st.column_config.ListColumn('languages', width='medium'),
        'codec': st.column_config.TextColumn('codec', disabled=True),
        'magnet': st.column_config.TextColumn('magnet', disabled=True),
    }
    msg = st.toast(f'searching for {search_str}...')
    df = tapi.query(torrent_search, site='kickass')
    df['size'] = df['size'].map(_togb, na_action='ignore')
    with search_col[0]:
        st.dataframe(
            data=df, 
            column_order=list(column_config.keys()),
            column_config=column_config,
            use_container_width=True,
            hide_index=True
        )
    msg.toast('search complete')


@st.cache_data
def display_images_in_grid(genre, columns):
    st.header(f'{genre.upper()} MOVIES')
    log.info(f'building image page for {genre} movies')
    for index, (movie, url) in enumerate(_cover_urls(genre=genre)):
        if index % columns == 0: 
            cols = st.columns(columns, gap='small')
        with cols[index % columns]:
            st.image(url, use_column_width=True)
            _year = _decode(movie[b'original air date'])
            _year = _year.replace('(', ' - ').replace(')', '')
            _title = _decode(movie[title_key])
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


log = clogger.log(os.getenv('LOG_LEVEL'), logger_name=__name__)
log.propagate = False
cover_key = b'full-size cover url'
title_key = b'title'
tapi = Clutch()
st.set_page_config(
    page_title=f'SPIN',
    initial_sidebar_state='auto',
    menu_items=None,
    page_icon=None,
    layout='wide', 
)
db = Database(decode=False)
genres = db.genres
tabs = st.tabs(('__SEARCH__', *genres))
genres = ('SEARCH', *genres)
tabs = {genre: tab for genre, tab in zip(genres, tabs)}
movie_columns = 6

with tabs['SEARCH']:
    st.title('TORRENT-API SEARCH')
    col_text, col_button = st.columns([4, 1])
    df_col = st.columns(1)
    with col_text:
        torrent_search = st.text_input(
            label='torrent search', value='', 
            help='search for a torrent by name using torrent-API'
        )
    with col_button:
        search_button = st.button(
            'search', key='search', 
            help='search for torrent with torrent-API',
            use_container_width=False,
            on_click=search_cb, args=(torrent_search, df_col)
        )


for genre, tab in tabs.items():
    with tab:
        if genre == 'SEARCH':
            continue 
        else:
            display_images_in_grid(genre, movie_columns)

