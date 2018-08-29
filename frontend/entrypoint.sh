#!/bin/bash
if [ $DEV = "true" ]; then
  yarn --pure-lockfile --ignore-optional
  yarn start
else
  yarn
  yarn build
  yarn serve
fi

