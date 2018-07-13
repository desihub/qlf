
#!/bin/sh
if [ -z "$1" ]; then
	docker-compose -f frontend/docker-compose.yml stop
	docker-compose -f backend/docker-compose.yml stop
  exit 1
fi

if [ $1 = "backend" ]; then
	CURRENT_UID=$(id -u):$(id -g) docker-compose -f backend/docker-compose.yml stop
else 
  if [ $1 = "frontend" ]; then
    CURRENT_UID=$(id -u):$(id -g) docker-compose -f frontend/docker-compose.yml stop
  fi
fi