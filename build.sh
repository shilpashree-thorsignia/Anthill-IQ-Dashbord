#!/bin/bash

# Upgrade pip
python -m pip install --upgrade pip

# Install build dependencies
pip install --upgrade setuptools wheel

# Install psycopg2 dependencies
apt-get update
apt-get install -y libpq-dev python3-dev

# Install requirements with --no-cache-dir to avoid wheel issues
pip install --no-cache-dir -r requirements.txt 