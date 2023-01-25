docker stop books-manager-container
docker rm books-manager-container

docker build . -t books-manager
docker run --name books-manager-container -p 8000:8000/tcp books-manager