#!/bin/bash
source ./venv/bin/activate && pip install invoke pip-tools && inv sync
tail -f /dev/null