#!/bin/bash
if [ $DEV = "true" ]; then
  yarn
  yarn start
else
  yarn serve
fi

