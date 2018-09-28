#!/bin/bash
if [ $DEV = "true" ]; then
  yarn --pure-lockfile --ignore-optional
  yarn start
else
  yarn --pure-lockfile --ignore-optional
  yarn build
fi

