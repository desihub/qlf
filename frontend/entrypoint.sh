#!/usr/bin/env sh
if [ $DEV = "true" ]; then
  bash
  yarn global add create-react-app
  cd src
  chown node:node -R .
  yarn install
  yarn start
else
  bash
  yarn global add create-react-app
  yarn global add util.promisify
  cd src
  chown node:node -R .
  yarn install
  yarn build
  yarn global add serve
  serve -s ../build -l $QLF_UI_PORT
fi
