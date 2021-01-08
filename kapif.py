import asyncio
import logging
import os
import time

from fastapi import FastAPI

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
        await asyncio.sleep(5)


@app.on_event("startup")
async def on_startup():
    logging.basicConfig(level=logging.INFO)

    log.info("Set up poll loop.")
    asyncio.ensure_future(poll_load())


@app.get("/")
async def index():
    return {
        "message": "hello world",
    }


@app.get("/cpu_load")
def get_cpu_load():
    return {"loads": load_db}
