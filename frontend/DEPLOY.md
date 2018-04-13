# Deployment

_This is an deployment example using `docker`, `nginx` on a linux machine._

_Also we assume that the domain is already correctly configured pointing to the correct machine._

1. Install [Nginx](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)

2. Add `qlf.conf` to `/etc/nginx/conf.d/` with the following configuration

_Assuming [qlf](https://github.com/desihub/qlf/blob/master/DEPLOY.md) is already configured_

```diff
    server {
        listen 80;
        server_name ql.linea.gov.br;

...

+        location / {
+            proxy_http_version 1.1;
+            proxy_buffering off;
+            proxy_redirect off;
+            proxy_set_header   X-Real-IP $remote_addr;
+            proxy_set_header   Host      $http_host;
+            proxy_pass         http://ql.linea.gov.br:3000/;
+        }
    }
```

3. Add prefered domain to [`docker-compose.yml`](https://github.com/desihub/qlf-ui/blob/master/docker-compose.yml)

_In this example we changed `localhost` to `ql.linea.gov.br`_

```
version: "3"

services:
  qlf-ui:
    build: .
    container_name: qlf-ui
    entrypoint: sh entrypoint.sh
    working_dir: /home/node
    ports:
      - 3000:3000
    volumes:
      - .:/home/node
```

_We assume you are running using `docker`_

4. Port `3000` must be open.

5. Restart nginx

`sudo service nginx restart`

6. In case `qlf api` is running on a different machine make sure you change [REACT_APP_WEBSOCKET and REACT_APP_BOKEH](https://github.com/desihub/qlf-ui/blob/master/.env) to the correct address

Example `.env`:

```
REACT_APP_WEBSOCKET=ws://ql.linea.gov.br/api
REACT_APP_BOKEH=http://ql.linea.gov.br/dashboard/
```
