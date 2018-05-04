#!/bin/bash

virtualenv --no-site-packages -p /usr/bin/python3 env
source env/bin/activate
pip install -r requirements.txt
echo "Virtual environment created."
