service redis-server start && \
service mysql start && \

# python3.11 -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt && \
python3.11 user_database_conn.py && \
# python3.11 server.py 
tail -f /dev/null