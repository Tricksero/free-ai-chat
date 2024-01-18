#!/bin/bash
source ./venv/bin/activate && pip install --upgrade pip && pip install invoke pip-tools && inv sync
tail -f /dev/null