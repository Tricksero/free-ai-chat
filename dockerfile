FROM python:3.9-bookworm


RUN apt-get update && apt upgrade -y

RUN apt-get update && apt install -y python3.11-venv
#&& apt-get install -y redis-server libpcap0.8

WORKDIR /gpt4all

COPY ./setup.sh /setup.sh

EXPOSE 8000

#RUN python -m venv venv && \
#. venv/bin/activate && \
#pip install -r requirements.txt && \
#python gpt4all_test.py
RUN python3.11 -m venv venv
RUN ./venv/bin/activate && pip install invoke pip-tools && inv sync
RUN chmod +x /setup.sh


CMD ["/bin/bash", "-c", "/setup.sh"]
