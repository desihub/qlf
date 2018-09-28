#!/bin/sh
docker-compose stop app
docker-compose up -d --force-recreate nginx 
