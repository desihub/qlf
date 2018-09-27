
#!/bin/sh
if [ -z "$1" ]; then
	docker-compose stop
  exit 1
fi
