#!/bin/bash
# Deployment Script for Patty M Designs API (Dreamhost VPS - No Sudo)

set -e  # Exit on any error

echo "=== Patty M Designs API - Deployment ==="
echo ""
echo "NOTE: This script is for Dreamhost VPS (no sudo access)"
echo "For complete deployment guide, see DREAMHOST_VPS_SETUP.md"
echo ""

# Check if we're in the right directory
if [ ! -f "deployment/start_server.sh" ]; then
    echo "Error: Must run from pmd_editor directory"
    exit 1
fi

# Start the server
echo "Step 1: Starting Gunicorn server..."
./deployment/start_server.sh

echo ""
echo "=== Deployment Complete! ==="
echo ""
echo "IMPORTANT: Configure Dreamhost Proxy Server"
echo "  1. Log into Dreamhost Panel"
echo "  2. Go to: Servers → VPS → Proxy Server"
echo "  3. Add Proxy: api.pattymdesigns.com → port 8001"
echo "  4. Wait for installation to complete"
echo ""
echo "Useful commands:"
echo "  - Check status: ./deployment/status.sh"
echo "  - Restart: ./deployment/restart_server.sh"
echo "  - Stop: ./deployment/stop_server.sh"
echo "  - View logs: tail -f ~/api.pattymdesigns.com/logs/gunicorn_error.log"
