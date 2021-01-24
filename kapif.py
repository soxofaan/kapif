import asyncio
import contextlib
import logging
import os
import sqlite3
import time

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

log = logging.getLogger(__name__)

app = FastAPI()

# TODO: get config from command line or external file?
config = {
    "database": "kapif.db",
    "poll_sleep": 60,
}


# TODO: encapsulate DB stuff better.
@contextlib.contextmanager
def db():
    con = sqlite3.connect(config["database"])
    yield con
    con.commit()
    con.close()


def db_setup():
    with db() as con:
        tables = set(row[0] for row in con.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())
        log.info(f"db_setup: tables in db: {tables}")
        if "cpu_load" not in tables:
            log.info("Creating table cpu_load")
            con.execute("CREATE table cpu_load(ts INT, load1 REAL, load5 REAL, load15 REAL)")
            # TODO: index on ts?
            con.commit()


async def poll_load():
    log.info("Start polling CPU load")
    while True:
        # TODO: log "still polling" message from time to time
        timestamp = int(time.time())
        cpu_load = os.getloadavg()
        with db() as con:
            con.execute("INSERT INTO cpu_load VALUES (?,?,?,?)", (timestamp,) + cpu_load)
        # TODO: make sleep delay configurable
        await asyncio.sleep(config["poll_sleep"])


@app.on_event("startup")
async def on_startup():
    logging.basicConfig(level=logging.INFO)

    db_setup()

    log.info("Set up poll loop.")
    asyncio.ensure_future(poll_load())


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def index():
    return RedirectResponse(url='/static/index.html')


@app.get("/cpu_load")
def get_cpu_load():
    # TODO: also poll load when handling this request?
    with db() as con:
        since = int(time.time() - 24 * 60 * 60)
        loads = [
            (row[0], row[1:])
            for row in con.execute("SELECT * FROM cpu_load WHERE ts > ?", (since,)).fetchall()
        ]
    return {
        "loads": loads,
        "series": ["load1", "load5", "load15"]
    }
