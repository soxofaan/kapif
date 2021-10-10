![status - alpha](https://img.shields.io/badge/status-alpha-red)


# Kapif - simple CPU load monitoring tool

Kapif is a very simple CPU load monitoring tool. There is just a single process that polls for the CPU load, stores that
in a simple sqlite databases and provides a simple web app for visualisation.

Intended to be used on a Raspberry Pi.

Requires Python 3.7 or higher.

Also just an excuse to play a bit with [FastAPI](https://fastapi.tiangolo.com/).

## Setup

Use some kind of Python virtual environment, e.g. `venv`:

    python3 -m venv venv
    . venv/bin/activate

And install dependencies in virtual environment:

    pip install -r requirements.txt

## Usage

1. Activate virtual env first, e.g.:

        . venv/bin/activate

2. Basic run:

        uvicorn kapif:app

   Check the docs of [uvicorn](https://www.uvicorn.org/)
   for more options and fine-tuning).

   For example, run with in background, listening on `0.0.0.0`, port 8888:

        nohup nice uvicorn --host 0.0.0.0 --port 8888 kapif:app 2>&1 > kapif.log < /dev/null &

3. Visit the webapp, depending on where/how you started it, e.g. at http://localhost:8000 if you run it in the most
   basic way locally. Note that you have to wait a couple of minutes to see anything useful because kapif polls the CPU
   load only every x minutes.
