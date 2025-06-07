#!/bin/bash

# Exit on error
set -e

# Initialize database
flask db upgrade

# Start the application
exec gunicorn -w 4 -b 0.0.0.0:8000 run:app