#!/bin/bash

cmd=$1



usage() {
    echo "deploy.sh <command> <arguments>"
    echo "Available commands:"
    echo " compose_up           up docker compose"
    echo " compose_down         down docker compose"
}

if [[ -z "$cmd" ]]; then
    echo "Missing command"
    usage
    exit 1
fi


compose_up() {
    docker-compose --env-file ./deployment/.env -f ./deployment/docker-compose.yml up -d
}

compose_down() {
    docker-compose --env-file ./deployment/.env -f ./deployment/docker-compose.yml down
}


case $cmd in
compose_up)
    compose_up "$@"
    ;;
compose_down)
    compose_down "$@"
    ;;
*)
    echo -n "Unknown command: $cmd"
    usage
    exit 1
    ;;
esac