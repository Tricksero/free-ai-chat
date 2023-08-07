# sudo bash create_new_container.sh
# service docker start
docker stop $(docker ps -a -q --filter "ancestor=aktuelles_projekt")
docker rm $(docker ps -a -q --filter "ancestor=aktuelles_projekt")
docker rmi aktuelles_projekt
docker build -t aktuelles_projekt .
docker run -d -ti -p 8000:8000 --name test aktuelles_projekt 
docker exec -ti test bash 


# curl -X POST -d '{"search":"london"}' -b 'PHPSESSID=c1nsa6op7vtk7kdis7bcnbadf1' -H 'Content-Type: application/json' http://<SERVER_IP>:<PORT>/search.php