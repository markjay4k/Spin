#!/usr/bin/env python3

from urllib.parse import unquote
from fastapi import FastAPI
from tagent import Agent
import uvicorn
import __init__
import os


app = FastAPI(docs_url=None)
agent = Agent()


@app.get("/ping")
async def ping():
    return {'ping': 'successful'}


@app.get("/download/{magnet}")
async def download_torrent(magnet: str):
    magnet = unquote(magnet)
    agent.download(magnet=magnet)
    return {"magnet": magnet}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.getenv('TORRENT_API_HOST'),
        port=os.getenv('TAGENT_PORT'),
        log_level=os.getenv('LOG_LEVEL').lower()
    )
