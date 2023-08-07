FROM ubuntu

RUN apt update && \
    apt upgrade && \
    apt install -y python3.11 \
    python3.11-venv 

#  
# mysql-client
RUN apt-get update && apt upgrade && \
    apt install -y mysql-server \
    mysql-client

# eventuell COPY config

# Configure MySQL and create user
RUN service mysql start \
    && mysql -e "CREATE USER 'test'@'localhost' IDENTIFIED BY '1234';" \
    && mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'test'@'localhost' WITH GRANT OPTION;" \
    && mysql -e "FLUSH PRIVILEGES;"

RUN apt-get update && apt-get install -y redis-server

# eventuell COPY config

# Wechseln zum Arbeitsverzeichnis im Container
WORKDIR /project


# Kopieren der Dateien in das Arbeitsverzeichnis im Container
COPY /project /project

EXPOSE 8000

# COPY /gpt4all /root/.cache 
#dumme idee dauert länger als neuer download

# Definieren eines Volumes, das den Ordner im Container mit dem Host-System verbindet
# VOLUME /project

RUN python3.11 -m venv venv && \
    . venv/bin/activate && \
    pip install -r requirements.txt && \
    python3.11 gpt4all_test.py 
#     python3.11 server.py

RUN chmod +x setup.sh


CMD ["/bin/bash", "-c", "./setup.sh"]
# CMD ["tail", "-f", "/dev/null"]
# RUN chmod +x /restart_services.sh
# CMD ["/restart_services.sh"]
