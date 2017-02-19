#!/bin/sh

bokeh serve --allow-websocket-origin=localhost:8000 dashboard/bokeh/metrics.py
