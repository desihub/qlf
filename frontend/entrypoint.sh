#!/bin/bash
if [ $DEV = "true" ]; then
  cd src
  chown node:node -R .
  yarn install
  yarn start
else
  cd src
  chown node:node -R .
  yarn install
  yarn build
  serve -s ../build -l $QLF_UI_PORT
fi
