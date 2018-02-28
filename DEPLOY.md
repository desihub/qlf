# Deployment

_This is an deployment example using `docker`, `nginx` on a linux machine._

_Also we assume that the domain is already correctly configured pointing to the correct machine._

1. Install [Nginx](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)

2. Add `qlf.conf` to `/etc/nginx/conf.d/` with the following configuration

```
    error_log /var/log/nginx/ql.linea.gov.br.log error;
    access_log /var/log/nginx/ql.linea.gov.br.log;
    # Create an upstream alias to where we've set daphne to bind to
    upstream websocket {
        server ql.linea.gov.br:8000;
    }


    server {
        listen 80;
        server_name ql.linea.gov.br;

        location /dashboard {
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_http_version 1.1;
            proxy_buffering off;
            proxy_redirect off;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   Host      $http_host;
            proxy_pass         http://ql.linea.gov.br:8000/dashboard;
        }

        location /start {
            proxy_pass         http://ql.linea.gov.br:8000/start;
        }

        location /stop {
            proxy_pass         http://ql.linea.gov.br:8000/stop;
        }

        location /api {
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_http_version 1.1;
            proxy_buffering off;
            proxy_redirect off;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   Host      $http_host;
            proxy_pass         http://ql.linea.gov.br:8000/;
        }
    }
```

3. Add prefered domain to [`docker-compose.yml`](https://github.com/desihub/qlf/blob/master/docker-compose.yml)

_In this example we changed `localhost` to `ql.linea.gov.br`_

```
version: '3'
services:
  qlf:
    build: .
    environment:
      - QLF_BASE_URL=http://ql.linea.gov.br
      - BOKEH_SERVER=ql.linea.gov.br
      - QLF_HOSTNAME=ql.linea.gov.br
      - QLF_API_URL=http://ql.linea.gov.br:8000/dashboard/api/
      - QLF_ROOT=/app/
      - DESI_SPECTRO_DATA=/app/spectro/data
      - DESI_SPECTRO_REDUX=/app/spectro/redux
      - QL_SPEC_DATA=/app/spectro/data
      - QL_SPEC_REDUX=/app/spectro/redux
      - OMP_NUM_THREADS=1 # This avoids unwanted concurrency during BoxcarExtract
    volumes:
      - .:/app
    restart: always
    working_dir: /app/
    command: ./run.sh
    ports:
      - "8000:8000"
      - "5006:5006"
      - "56005:56005"
    links:
      - redis
  redis:
    image: redis
    ports:
      - "6379"
```

_We assume you followed the [docker installations steps](https://github.com/desihub/qlf/blob/master/DOCKER.md) already._

4. Ports `5006`, `8000` must be open.

`5006` is used by `bokeh` to show plots
`8000` is used by `django api`

5. Restart nginx

`sudo service nginx restart`
