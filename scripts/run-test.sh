#!/bin/bash

set -exo pipefail

export PYTHONPATH=src/.

python3 src/test/test.py