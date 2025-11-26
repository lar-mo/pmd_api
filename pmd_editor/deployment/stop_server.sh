#!/bin/bash
# Stop Gunicorn server

if [ ! -f /home/lar_mo/api.pattymdesigns.com/logs/gunicorn.pid ]; then
    echo "Server is not running (no PID file found)"
    exit 1
fi

PID=$(cat /home/lar_mo/api.pattymdesigns.com/logs/gunicorn.pid)

if ! ps -p $PID > /dev/null 2>&1; then
    echo "Server is not running (stale PID file)"
    rm /home/lar_mo/api.pattymdesigns.com/logs/gunicorn.pid
    exit 1
fi

echo "Stopping server (PID: $PID)..."
kill $PID

# Wait for graceful shutdown
for i in {1..10}; do
    if ! ps -p $PID > /dev/null 2>&1; then
        echo "Server stopped successfully"
        rm -f /home/lar_mo/api.pattymdesigns.com/logs/gunicorn.pid
        exit 0
    fi
    sleep 1
done

# Force kill if still running
if ps -p $PID > /dev/null 2>&1; then
    echo "Force killing server..."
    kill -9 $PID
    rm -f /home/lar_mo/api.pattymdesigns.com/logs/gunicorn.pid
fi

echo "Server stopped"
