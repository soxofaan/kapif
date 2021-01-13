
# Kapif - simple CPU load monitoring tool

Kapif is a very simple CPU load monitoring tool.
There is just a single process that polls for the CPU
load, stores that in a simple sqlite databases
and provides a simple web app for visualisation.

Intended to be used on a Raspberry Pi.

Requires Python 3.7 or higher.

Setup, in some kind of virtual environment:

    pip install -r requirements.txt


Run:

    uvicorn kapif:app

Run with in background:

    nohup nice uvicorn kapif:app 2>&1 > kapif.log < /dev/null &
