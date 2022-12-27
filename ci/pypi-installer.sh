#!/usr/bin/env bash


python -m pip install --upgrade pip
pip install numpy<1.24 lxml
pip install -r requirements-dev.txt
pip install -r requirements.txt

if [[ "$PANDAS" == "MASTER" ]]; then
  PRE_WHEELS="https://7933911d6844c6c53a7d-47bd50c35cd79bd838daf386af554a83.ssl.cf2.rackcdn.com"
  pip install --pre --upgrade --timeout=60 -f "$PRE_WHEELS" pandas --user
else
  pip install pandas=="$PANDAS"
fi

if [[ ! -z "$NUMPY" ]]; then
  pip install --upgrade --force-reinstall numpy=="$NUMPY"
fi