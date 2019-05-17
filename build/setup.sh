#!/bin/bash

python3 -m venv venv
cd venv; source bin/activate; cd ..
pip3 install -r requirements.txt
cd ..

