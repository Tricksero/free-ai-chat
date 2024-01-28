#source venv/bin/activate && \
pip install pip-tools invoke
inv sync
tail -f /dev/null