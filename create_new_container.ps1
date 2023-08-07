# powershell.exe -ExecutionPolicy Bypass -File .\create_new_container.ps1

# Remove-Item -Path .\project\response.txt

# Remove-Item -Path .\project\venv -recurse

docker stop $(docker ps -a -q --filter "ancestor=aktuelles_projekt") # das durch einen container bzw image namen ersetzen

docker rm $(docker ps -a -q --filter "ancestor=aktuelles_projekt")

docker rmi aktuelles_projekt

docker volume prune -f

docker build -t aktuelles_projekt . 

# docker run -d -ti --cpus=2 --memory 1G aktuelles_projekt 
docker run -d -ti aktuelles_projekt 

$containerid=$(docker ps -a -q --filter "ancestor=aktuelles_projekt")

# docker cp ${containerid}:/project/response.txt ./project

# docker cp ${containerid}:/root/.cache/gpt4all ./gpt4all

docker exec -ti ${containerid} bash 
 


# sudo docker build -t aktuelles_projekt . && sudo docker run -d -ti --name test aktuelles_projekt && sudo docker exec -ti test bash 
# sudo docker stop test && sudo docker system prune --all