#!/bin/sh
docker-compose -f frontend/docker-compose.yml stop
CURRENT_UID=$(id -u):$(id -g) docker-compose -f backend/docker-compose.yml up -d
