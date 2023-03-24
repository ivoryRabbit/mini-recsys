#!/bin/bash

set -exo pipefail

export PYTHONPATH=src/.

gunicorn src.app.main:app -b 0.0.0.0:5000 -k "uvicorn.workers.UvicornWorker" --timeout=60