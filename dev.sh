#!/bin/bash

export ROLE="$1"
export PROFILE="DEV"
export LOGGING_LEVEL="DEBUG"
if [[ $ROLE == "" ]]; then
    export ROLE="default"
fi
if [[ -f env.sh ]]; then
  source env.sh
fi
if [[ $PROFILE != "" ]] && [[ $ROLE != "" ]]; then
  cd app || exit 1
  poetry run python main.py
  exit 0
else
  echo "Error:"
  if [[ $ROLE == "" ]]; then
      echo "> ROLE is unset"
  fi
  exit 1
fi
