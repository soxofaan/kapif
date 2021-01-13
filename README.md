
# Kapif - simple CPU load monitoring tool

Kapif is a very simple CPU load monitoring tool.
There is just a single process that polls for the CPU
load, stores that in a simple sqlite databases
and provides a simple web app for visualisation.

Intended to be used on a Raspberry Pi.

Requires Python 3.7 or higher.

## Setup and usage

Use some kind of Python virtual environment, e.g. `venv`:

    python3 -m venv venv
    . venv/bin/activate

Install depdendencies in virtual environment:

    pip install -r requirements.txt

Basic run:

    uvicorn kapif:app

Run with in background, listening on `0.0.0.0`:

    nohup nice uvicorn --host 0.0.0.0 kapif:app 2>&1 > kapif.log < /dev/null &

