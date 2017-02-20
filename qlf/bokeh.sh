#!/bin/sh
export PYTHONPATH=$PYTHONPATH:.
bokeh serve --allow-websocket-origin=localhost:8000 dashboard/bokeh/qa-snr
