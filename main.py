from urllib.parse import unquote
from fastapi import FastAPI
from tagent import Agent
import uvicorn


app = FastAPI(docs_url=None)
agent = Agent()


@app.get("/download/{magnet}")
async def download_torrent(magnet: str):
    magnet = unquote(magnet)
    agent.download(magnet=magnet)
    return {"magnet": magnet}


if __name__ == "__main__":
    uvicorn.run(app, host='192.168.10.67', port=5000, log_level="info")
