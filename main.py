from fastapi import FastAPI
from tagent import Tagent
import uvicorn


app = FastAPI()
agent = Tagent()


@app.get('/download/{magnet}')
async def download_torrent(magnet):
    agent.download(magnet)
    return {'magnet': magnet}


if __name__ == "__main__":
    uvicorn.run("main:app", host='192.168.10.67', port=5000, log_level="info")
