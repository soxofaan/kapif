import asyncio
import logging
import os
import time

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

log = logging.getLogger(__name__)

app = FastAPI()

load_db = []


async def poll_load():
    global load_db
    log.info("Start polling CPU load")
    while True:
        # TODO: log "still polling" message from time to time
        timestamp = int(time.time())
        cpu_load = os.getloadavg()
        load_db.append((timestamp, cpu_load))
        # TODO: make sleep delay configurable
        await asyncio.sleep(5)


@app.on_event("startup")
async def on_startup():
    logging.basicConfig(level=logging.INFO)

    log.info("Set up poll loop.")
    asyncio.ensure_future(poll_load())


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def index():
    return RedirectResponse(url='/static/index.html')


@app.get("/cpu_load")
def get_cpu_load():
    return {
        "loads": load_db,
        "series": ["load1", "load5", "load15"]
    }
