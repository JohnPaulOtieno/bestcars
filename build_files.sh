#!/usr/bin/env bash
# Vercel build script — runs during every deployment
set -e

pip install -r requirements.txt
python manage.py collectstatic --noinput --clear
python manage.py migrate --noinput
