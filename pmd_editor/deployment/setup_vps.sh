#!/bin/bash
# VPS Setup Script for Patty M Designs API (No sudo required)

set -e  # Exit on any error

echo "=== Patty M Designs API - VPS Setup ==="
echo ""

# Create virtual environment
echo "Step 1: Creating Python virtual environment..."
cd /home/lar_mo/api.pattymdesigns.com
virtualenv -p python3 venv

# Activate virtual environment and install dependencies
echo ""
echo "Step 2: Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r pmd_editor/requirements.txt

# Create log directories in user space
echo ""
echo "Step 3: Creating log directories..."
mkdir -p /home/lar_mo/api.pattymdesigns.com/logs

# Collect static files
echo ""
echo "Step 4: Collecting Django static files..."
cd pmd_editor
python manage.py collectstatic --noinput

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Next steps:"
echo "1. Edit secrets.json with production values"
echo "2. Update settings.py (set DEBUG=False)"
echo "3. Start the server: ./deployment/start_server.sh"
