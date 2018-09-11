#!/bin/sh
if [ -z "$1" ]; then
  echo "Ajusting version..."
  printf '%q\n' $(awk '!/REACT_APP_VERSION/' frontend/.env) > frontend/.env
  echo "REACT_APP_VERSION=$(git log --pretty=format:"%h %ai" -1)" >> frontend/.env
  echo "Staring backend... http://localhost/dashboard/api/"
  echo "Building frontend... http://localhost"
  echo "It may take a few minutes to start..."
  CURRENT_UID=$(id -u):$(id -g) docker-compose up --force-recreate -d
  exit 1
fi

if [ $1 = "logs" ]; then
  printf '%q\n' $(awk '!/REACT_APP_VERSION/' frontend/.env) > frontend/.env
  echo "REACT_APP_VERSION=$(git log --pretty=format:"%h %ai" -1)" >> frontend/.env
  CURRENT_UID=$(id -u):$(id -g) docker-compose up --force-recreate
  exit 1
fi

if [ $1 = "daemon" ]; then
  docker exec -it $(docker ps -f "name=qlf" --format "{{.Names}}") ./startDaemon.sh
fi
