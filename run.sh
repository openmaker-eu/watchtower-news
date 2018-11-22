#!/usr/bin/env bash

eval $(cat .env | sed 's/^/export /')

echo "$(whoami)"

[ "$UID" -eq 0 ] || exec sudo "$0" "$@"

docker-compose down
docker-compose up -d --scale rq-worker=$(grep WORKER_NUMBER .env | cut -d '=' -f2)
