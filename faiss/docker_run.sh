docker run -it -d --rm --gpus all --name faiss --net host -v $(pwd):/home   faiss:latest

docker run -it -d --rm --gpus all --name server --net host -v /mmlabworkspace:/mmlabworkspace   faiss:latest