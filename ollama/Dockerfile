FROM debian:bookworm

RUN apt-get update && apt upgrade -y

RUN apt install -y curl

RUN curl -L https://ollama.ai/download/ollama-linux-amd64 -o /usr/bin/ollama

RUN chmod +x /usr/bin/ollama

# RUN apt install -y nginx
# COPY ./nginx.conf ./nginx.conf
# RUN cat ./nginx.conf >> /etc/nginx/sites-enabled/default
# EXPOSE 9000
EXPOSE 11434
ENV OLLAMA_HOST=0.0.0.0:11434
COPY ./entrypoint.sh ./entrypoint.sh
RUN chmod 0777 ./entrypoint.sh
CMD [ "./entrypoint.sh" ]
# CMD ["/usr/bin/ollama", "serve"]
# CMD ["/bin/bash", "-c", "/usr/bin/ollama serve && service nginx start"]
