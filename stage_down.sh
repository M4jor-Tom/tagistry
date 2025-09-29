#!/bin/bash

if [[ -f env.sh ]]; then
  source env.sh
fi
docker compose down
