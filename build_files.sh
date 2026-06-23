#!/usr/bin/env bash
# Vercel build script — runs during every deployment
set -e

pip install -r requirements.txt --break-system-packages
python manage.py collectstatic --noinput --clear
python manage.py migrate --noinput
