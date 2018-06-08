#!/bin/bash
if [ $DEV = "true" ]; then
  yarn start
else
  yarn serve
fi

