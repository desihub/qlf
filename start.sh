
#!/bin/sh
if [ -z "$1" ]; then
  docker-compose -f frontend/docker-compose.yml up -d
  docker-compose -f backend/docker-compose.yml up
  exit 1
fi

if [ $1 = "backend" ]; then
	docker-compose -f backend/docker-compose.yml up
else 
  if [ $1 = "frontend" ]; then
  	docker-compose -f frontend/docker-compose.yml up
  fi
fi

if [ $1 = "prod" ]; then
  cd frontend
  sed -i '/REACT_APP_VERSION/d' .env
  echo "REACT_APP_VERSION=$(git rev-parse HEAD)" >> .env
  cd ..
  docker-compose -f frontend/docker-compose.yml up -d
	docker-compose -f backend/docker-compose.yml up -d
fi