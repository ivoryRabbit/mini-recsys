#!/bin/bash

set -exo pipefail

export PYTHONPATH=src/.

python3 src/app/main.py