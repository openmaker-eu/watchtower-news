#!/usr/bin/env bash

docker-compose down
docker-compose up -d --scale rq-worker=$(grep WORKER_NUMBER .env | cut -d '=' -f2)
