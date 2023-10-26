#!/bin/bash
cd /home/rami/nicecv
source venv/bin/activate
python manage.py dbbackup
mkdir /home/rami/backups/nicecv/$(date +%Y-%m-%d)
python manage.py dumpdata > /home/rami/backups/nicecv/$(date +%Y-%m-%d)/db.json