
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
  if git describe --exact-match --tags $(git log -n1 --pretty='%h') ; then
      echo "REACT_APP_VERSION=$(git describe --exact-match --tags $(git log -n1 --pretty='%h'))" >> .env
  else
      echo "REACT_APP_VERSION=$(git log --pretty=format:"%h %ai" -1)" >> .env
  fi
  cd ..
  docker-compose -f frontend/docker-compose.yml up -d
	docker-compose -f backend/docker-compose.yml up -d
fi

if [ $1 = "bokeh" ]; then
  docker exec -it $(docker ps -f "name=qlf" --format "{{.Names}}") ./startBokeh.sh
fi

if [ $1 = "daemon" ]; then
  docker exec -it $(docker ps -f "name=qlf" --format "{{.Names}}") ./startDaemon.sh
fi
