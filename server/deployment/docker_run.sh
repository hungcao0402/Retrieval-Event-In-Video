docker run -it -d --rm --gpus all --name server --net host -v $(pwd):/home   faiss:latest
