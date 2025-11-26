#!/bin/bash
# Restart Gunicorn server

echo "Restarting server..."
/home/lar_mo/api.pattymdesigns.com/pmd_editor/deployment/stop_server.sh
sleep 2
/home/lar_mo/api.pattymdesigns.com/pmd_editor/deployment/start_server.sh
