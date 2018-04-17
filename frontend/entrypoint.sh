#!/usr/bin/env sh
if [ $DEV = "true" ]; then
  bash
  yarn global add create-react-app
  create-react-app src
  cd src
  chown node:node -R .
  yarn install
  yarn start
else
  bash
  yarn global add create-react-app
  create-react-app src
  cd src
  chown node:node -R .
  yarn install
  yarn build
  yarn global add serve
  serve -s /home/node/build -p $QLF_UI_PORT
fi
