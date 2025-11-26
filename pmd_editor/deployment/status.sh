#!/bin/bash
# Check server status

if [ ! -f /home/lar_mo/api.pattymdesigns.com/logs/gunicorn.pid ]; then
    echo "Status: NOT RUNNING (no PID file)"
    exit 1
fi

PID=$(cat /home/lar_mo/api.pattymdesigns.com/logs/gunicorn.pid)

if ps -p $PID > /dev/null 2>&1; then
    echo "Status: RUNNING (PID: $PID)"
    echo ""
    echo "Recent access log:"
    tail -5 /home/lar_mo/api.pattymdesigns.com/logs/gunicorn_access.log 2>/dev/null || echo "  (no access log yet)"
    echo ""
    echo "Recent error log:"
    tail -5 /home/lar_mo/api.pattymdesigns.com/logs/gunicorn_error.log 2>/dev/null || echo "  (no errors)"
else
    echo "Status: NOT RUNNING (stale PID file)"
    rm /home/lar_mo/api.pattymdesigns.com/logs/gunicorn.pid
    exit 1
fi
