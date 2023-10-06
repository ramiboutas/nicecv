#!/bin/bash
cd /home/rami/nicecv
source venv/bin/activate
python manage.py dbbackup
