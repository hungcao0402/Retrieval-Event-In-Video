#!/bin/bash

cmd=$1

# constants
IMAGE_NAME='faiss'
IMAGE_TAG='latest'

if [[ -z "$cmd" ]]; then
    echo "Missing command"
    exit 1
fi

run_faiss(){
    model_config_path=$1
    port=$2
    if [[ -z "$model_config_path" ]]; then
        echo "Missing model_config_path"
        exit 1
    fi
    if [[ -z "$port" ]]; then
        echo "Missing port"
        exit 1
    fi

    # docker build -f deployment/Dockerfile -t $IMAGE_NAME:$IMAGE_TAG .
    IMAGE_NAME=$IMAGE_NAME:$IMAGE_TAG  \
        MODEL_CONFIG_PATH=$model_config_path PORT=$port \
        docker-compose -f deployment/docker-compose.yml up -d
}

shift

case $cmd in
run_faiss)
    run_faiss "$@"
    ;;
*)
    echo -n "Unknown command: $cmd"
    exit 1
    ;;
esac