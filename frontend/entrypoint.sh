#!/bin/bash
if [ $DEV = "true" ]; then
  yarn --pure-lockfile --ignore-optional
  yarn start
else
  yarn serve
fi

