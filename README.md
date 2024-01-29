# SPIN

Display popular IMDb movies by genres, find torrents using [Torrent-Api-py](https://github.com/Ryuk-me/Torrent-Api-py),
and download by interfacing with [Transmission](https://github.com/transmission/transmission).

## CODE OVERVIEW 

- `spin.py`: CLI script used to download top40 movies by genre from IMDb
- `movies.py`: Interfaces with `Cinemagoer` to download movie metadata
- `red.py`: Interfaces with the Redis database docker container
- `_images.py`: downloads cover art, adds border to movies already in Jellyfin
- `__init__.py`: Starts Redis container if down and loads environment variables 
- `clogger.py`: logging module

