#!/bin/bash
# Start Gunicorn server in the background

cd /home/lar_mo/api.pattymdesigns.com/pmd_editor
source ../venv/bin/activate

# Check if already running
if [ -f ../logs/gunicorn.pid ]; then
    PID=$(cat ../logs/gunicorn.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "Server is already running (PID: $PID)"
        exit 1
    fi
fi

echo "Starting Gunicorn server..."
nohup gunicorn \
    --config /home/lar_mo/api.pattymdesigns.com/pmd_editor/deployment/gunicorn_simple.conf.py \
    pmd_editor.wsgi:application \
    > /home/lar_mo/api.pattymdesigns.com/logs/nohup.log 2>&1 &

sleep 2

if [ -f ../logs/gunicorn.pid ]; then
    PID=$(cat ../logs/gunicorn.pid)
    echo "Server started successfully (PID: $PID)"
    echo "Access log: ~/api.pattymdesigns.com/logs/gunicorn_access.log"
    echo "Error log: ~/api.pattymdesigns.com/logs/gunicorn_error.log"
else
    echo "Failed to start server. Check logs at:"
    echo "  ~/api.pattymdesigns.com/logs/nohup.log"
    exit 1
fi
