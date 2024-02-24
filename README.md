# SPIN

Display popular IMDb movies by genres, find torrents using [Torrent-Api-py](https://github.com/Ryuk-me/Torrent-Api-py),
and download by interfacing with [Transmission](https://github.com/transmission/transmission).

## INSTALL

```shell
git clone https://github.com/markjay4k/Spin.git
cd Spin
```
create a `.env` file

| `variable`             | `values`           |
|------------------------|--------------------|
| `SPIN_PATH`            | `./spin`           |
| `DOWNLOAD_COVER_IMAGE` | `0`                |
| `DATABASE_NETWORK`     | `redpanda`         |
| `DATABASE_NAME`        | `redpanda`         |
| `REDIS_EXPIRE_SECONDS` | `72000`            |
| `REDIS_IP_ADDR`        | `redpanda`         |
| `REDIS_PORT`           | `6379`             |
| `LOG_LEVEL`            | `INFO`             |
| `JF_MOVIE_DIR`         | `/jellyfin/media`  |
| `TORRENT_API_HOST`     | `localip`          |
| `TORRENT_API_PORT`     | `8009`             |
| `TORRENT_API_PATH`     | `./Torrent-Api-py` |
| `TAGENT_PORT`          | `5000`             |
| `TRANSMISSION_IP`      | `localip`          |
| `TRANSMISSION_PORT`    | `9091`             |
| `TRANSMISSION_USER`    | `user`             |
| `TRANSMISSION_PASS`    | `password`         |
| `CRON_SCHEDULE`        | `'0 4 * * *'`      |

## CODE OVERVIEW 

- `spin.py`: CLI script used to download top40 movies by genre from IMDb
- `movies.py`: Interfaces with `Cinemagoer` to download movie metadata
- `red.py`: Interfaces with the Redis database docker container
- `_images.py`: downloads cover art, adds border to movies already in Jellyfin
- `__init__.py`: Starts Redis container if down and loads environment variables 
- `clogger.py`: logging module

