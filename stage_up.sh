#!/bin/bash

if [[ -f env.sh ]]; then
  source env.sh
fi
if [[ $DEFAULT_CONTENT_FILE_DIR == "" ]]; then
  export DEFAULT_CONTENT_FILE_DIR="/var/tagistry/content_files"
fi
if [[ $DEFAULT_RULE_SET_DIR == "" ]]; then
  export DEFAULT_RULE_SET_DIR="/var/tagistry/rule_set"
fi
docker compose up --build
