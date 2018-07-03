
#!/bin/sh
if [ -z "$1" ]; then
  echo "Staring backend... $(awk -F'=' '/QLF_API_URL=/ {print $2}' backend/docker-compose.yml)"
  echo "Starting frontend... http://localhost:"$(awk -F'=' '/QLF_UI_PORT=/ {print $2}' frontend/docker-compose.yml)
  echo "It may take a few minutes to start..."
  CURRENT_UID=$(id -u):$(id -g) docker-compose -f frontend/docker-compose.yml up --force-recreate &
  CURRENT_UID=$(id -u):$(id -g) docker-compose -f backend/docker-compose.yml up --force-recreate &
  exit 1
fi

if [ $1 = "backend" ]; then
	CURRENT_UID=$(id -u):$(id -g) docker-compose -f backend/docker-compose.yml up --force-recreate
else 
  if [ $1 = "frontend" ]; then
    CURRENT_UID=$(id -u):$(id -g) docker-compose -f frontend/docker-compose.yml up --force-recreate
  fi
fi

if [ $1 = "prod" ]; then
  cd frontend
  printf '%q\n' $(awk '!/REACT_APP_VERSION/' .env) > .env
  if git describe --exact-match --tags $(git log -n1 --pretty='%h') ; then
      echo "REACT_APP_VERSION=$(git describe --exact-match --tags $(git log -n1 --pretty='%h'))" >> .env
  else
      echo "REACT_APP_VERSION=$(git log --pretty=format:"%h %ai" -1)" >> .env
  fi
  cd ..
  CURRENT_UID=$(id -u):$(id -g) docker-compose -f frontend/docker-compose.yml run --entrypoint="yarn build" frontend
  CURRENT_UID=$(id -u):$(id -g) docker-compose -f frontend/docker-compose.yml up -d --force-recreate
	CURRENT_UID=$(id -u):$(id -g) docker-compose -f backend/docker-compose.yml up -d --force-recreate
fi

if [ $1 = "bokeh" ]; then
  docker exec -it $(docker ps -f "name=qlf" --format "{{.Names}}") ./startBokeh.sh
fi

if [ $1 = "daemon" ]; then
  docker exec -it $(docker ps -f "name=qlf" --format "{{.Names}}") ./startDaemon.sh
fi
