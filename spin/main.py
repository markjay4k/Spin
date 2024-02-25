#!/usr/bin/env python3

from urllib.parse import unquote
from fastapi import FastAPI
from tr_rpc import Agent
import uvicorn
import os
import __init__


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


if __name__ == '__main__':
    config = uvicorn.Config(
        app,
        #host=os.getenv('RPC_API_HOST'),
        host=os.getenv('DATABASE_NETWORK'),
        port=int(os.getenv('RPC_API_PORT')),
        log_level=os.getenv('LOG_LEVEL').lower()
    )
    server = uvicorn.Server(config)
    server.run()

