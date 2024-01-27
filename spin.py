from movies import Movies
import argparse
import clogger
import time


def sync(args):
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
    genres = args.genre if args.genre else default_genres
    log = clogger.log('INFO')
    mov = Movies()
    log.info(f'type: {isinstance(genres, str)}')
    if isinstance(genres, str):
        genres = [genres]

    for genre in genres:
        try:
            log.info(f'updating movie database with {genre=}')
            mov.top50_by_genre(genre=genre)
            time.sleep(1)
        except Exception as error:
            log.warning(f'{error=}')
            log.warning(f'could not update {genre=}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-g', '--genre', type=str, default=None,
        help='pick a genre'
    )
    args = parser.parse_args()
    sync(args)
