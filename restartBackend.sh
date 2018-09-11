#!/bin/sh
docker-compose stop backend
CURRENT_UID=$(id -u):$(id -g) docker-compose up -d --force-recreate nginx 
