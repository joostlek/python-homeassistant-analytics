#!/bin/bash
. $NVM_DIR/nvm.sh
nvm install 20

npm install

poetry install
poetry run pre-commit install
