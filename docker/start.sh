#!/bin/sh
set -xe

# Detect the host IP
# export DOCKER_BRIDGE_IP=$(ip ro | grep default | cut -d' ' -f 3)

python manage.py migrate

exec python manage.py runserver 0.0.0.0:8000
