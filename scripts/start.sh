#!/bin/bash

cd /home/rami/nicecv
source venv/bin/activate
gunicorn --config config/gunicorn.conf.py --bind unix:/run/gunicorn_nicecv.sock config.wsgi:application
