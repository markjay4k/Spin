from movies import Movies
import argparse
import clogger
import time


def sync(args):
    genres = args.genres
    log = clogger.log('INFO')
    mov = Movies()
    for genre in genres:
        try:
            log.info(f'updating movie database with {genre=}')
            mov.top40_by_genre(genre=genre)
            time.sleep(1)
        except Exception as error:
            log.warning(f'{error=}')
            log.warning(f'could not update {genre=}')


if __name__ == '__main__':
    default_genres = [
        'horror',
        'drama',
        'sci-fi',
        'adventure',
        'comedy',
        'family',
        'romance',
        'thriller'
    ]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-g', '--genres', 
        nargs='*', default=default_genres,
        help=f'pick a genre',
        choices=default_genres
    )
    args = parser.parse_args()
    sync(args)
