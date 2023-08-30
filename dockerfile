FROM python:3.11.4-bullseye


RUN apt-get update && apt upgrade -y

RUN apt-get update && apt-get install -y redis-server

WORKDIR /gpt4all

COPY ./requirements ./requirements

COPY . .
COPY ./setup.sh /setup.sh

EXPOSE 8000

#RUN python -m venv venv && \
#. venv/bin/activate && \
#pip install -r requirements.txt && \
#python gpt4all_test.py

RUN ls
RUN chmod +x /setup.sh


CMD ["/bin/bash", "-c", "/setup.sh"]
