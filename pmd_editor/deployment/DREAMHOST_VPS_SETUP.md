# Dreamhost VPS Deployment Guide

Complete guide for deploying Django APIs to Dreamhost VPS (no sudo access).

## Reference

This guide is based on experience and the excellent article:
- [How to Deploy Django Project on Dreamhost VPS](https://www.linkedin.com/pulse/how-deploy-django-project-dreamhost-vps-bashar-ghadanfar-srpwf/) by Bashar Ghadanfar

## Overview

Dreamhost VPS is a managed environment where you don't have sudo access. This guide covers the specific steps needed to deploy a Django application.

## Prerequisites

- Dreamhost VPS account
- Domain/subdomain configured and pointing to VPS IP
- SSH access to VPS

## Part 1: VPS Setup

### 1. Create Directory Structure

When you add a domain in Dreamhost panel, it creates:
```
/home/YOUR_USERNAME/your.domain.com/
├── favicon.gif
├── favicon.ico
└── .dh-diag -> /dh/web/diag
```

### 2. Upload Your Django Project

Upload your project to the domain directory:

```bash
# From your local machine
scp -r your_django_project YOUR_USERNAME@YOUR_VPS:/home/YOUR_USERNAME/your.domain.com/
```

### 3. Set Up Python Virtual Environment

Dreamhost VPS uses `virtualenv` (not `python3 -m venv`):

```bash
ssh YOUR_USERNAME@YOUR_VPS
cd /home/YOUR_USERNAME/your.domain.com
virtualenv -p python3 venv
source venv/bin/activate
pip install --upgrade pip
pip install -r your_django_project/requirements.txt
```

### 4. Configure Django Settings

Edit `settings.py`:

```python
DEBUG = False

ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    '.yourdomain.com',  # Allows all subdomains
    'YOUR_VPS_IP'
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
```

### 5. Collect Static Files

```bash
cd your_django_project
python manage.py collectstatic --noinput
python manage.py migrate  # if needed
```

## Part 2: Start Gunicorn Server

### 1. Choose an Available Port

Common ports on shared VPS:
- Check what's in use: `lsof -i :PORT_NUMBER`
- Pick an unused port (e.g., 8001, 8002, etc.)

### 2. Create Gunicorn Config

Create `gunicorn.conf.py`:

```python
import multiprocessing

bind = "0.0.0.0:8001"  # Your chosen port
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 30
keepalive = 2

accesslog = "/home/YOUR_USERNAME/your.domain.com/logs/gunicorn_access.log"
errorlog = "/home/YOUR_USERNAME/your.domain.com/logs/gunicorn_error.log"
loglevel = "info"

proc_name = "your_api_name"
pidfile = "/home/YOUR_USERNAME/your.domain.com/logs/gunicorn.pid"
```

### 3. Create Start/Stop Scripts

**start_server.sh:**
```bash
#!/bin/bash
cd /home/YOUR_USERNAME/your.domain.com/your_django_project
source ../venv/bin/activate

if [ -f ../logs/gunicorn.pid ]; then
    PID=$(cat ../logs/gunicorn.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "Server is already running (PID: $PID)"
        exit 1
    fi
fi

echo "Starting Gunicorn server..."
nohup gunicorn \
    --config /home/YOUR_USERNAME/your.domain.com/your_django_project/gunicorn.conf.py \
    your_project.wsgi:application \
    > /home/YOUR_USERNAME/your.domain.com/logs/nohup.log 2>&1 &

sleep 2
echo "Server started successfully"
```

**stop_server.sh:**
```bash
#!/bin/bash
if [ ! -f /home/YOUR_USERNAME/your.domain.com/logs/gunicorn.pid ]; then
    echo "Server is not running"
    exit 1
fi

PID=$(cat /home/YOUR_USERNAME/your.domain.com/logs/gunicorn.pid)
kill $PID
rm -f /home/YOUR_USERNAME/your.domain.com/logs/gunicorn.pid
echo "Server stopped"
```

Make executable:
```bash
chmod +x start_server.sh stop_server.sh
```

### 4. Start Your Server

```bash
./start_server.sh
```

Test locally:
```bash
curl http://localhost:8001/
```

## Part 3: Configure Dreamhost Proxy (CRITICAL STEP!)

This is the step that connects your domain to your running application.

### 1. Log into Dreamhost Panel

Navigate to: **Servers → VPS → Proxy Server**

### 2. Add Proxy Configuration

Click **"Add Proxy Server"**

Fill in:
- **Domain**: `api.yourdomain.com` (or your subdomain)
- **Port**: `8001` (the port your Gunicorn is running on)

Click **"Add Proxy Now"**

### 3. Wait for Installation

The proxy will show "Installing..." status. This usually takes 5-15 minutes.

Once complete, it will show "Active" status.

### 4. Test Your API

```bash
# Test from local machine
curl https://api.yourdomain.com/
```

Your API should now be accessible via the domain!

## Part 4: Auto-Start on Reboot

Add to crontab to start server on VPS reboot:

```bash
crontab -e
```

Add:
```
@reboot /home/YOUR_USERNAME/your.domain.com/your_django_project/start_server.sh
```

## Part 5: SSL Certificate (Optional)

Dreamhost automatically provides SSL for domains. If SSL isn't working:

1. Go to **Websites → Manage Websites**
2. Find your domain
3. Click **"Manage"**
4. Look for **"Secure Hosting (HTTPS)"**
5. Enable **"Let's Encrypt SSL"**

## Maintenance

### View Logs
```bash
tail -f ~/your.domain.com/logs/gunicorn_error.log
tail -f ~/your.domain.com/logs/gunicorn_access.log
```

### Restart Server
```bash
./stop_server.sh
./start_server.sh
```

### Update Code
```bash
cd ~/your.domain.com/your_django_project
# Upload new files or git pull
source ../venv/bin/activate
python manage.py collectstatic --noinput
python manage.py migrate
./restart_server.sh
```

## Important: Worker Configuration for Self-Calling APIs

**⚠️ Critical for APIs that call themselves internally!**

If your API has wrapper endpoints that call internal endpoints on localhost (e.g., `/wrapper/pmdv3ProdGetStrings/` calls `http://localhost:8001/strings/v3/`), you **must use 2 or more workers**.

### The Problem: Deadlock with 1 Worker
```python
workers = 1  # ❌ BAD - causes deadlock
```

With only 1 worker:
1. Worker receives wrapper request
2. Worker tries to call localhost:8001 (itself)
3. **Deadlock!** Worker is waiting for itself to respond
4. Result: Worker timeout → 502/500 errors

### The Solution: Multiple Workers
```python
workers = 2  # ✅ GOOD - no deadlock
```

With 2+ workers:
1. Worker 1 receives wrapper request
2. Worker 1 calls localhost:8001
3. Worker 2 handles the internal request
4. Success!

**Symptoms of this issue:**
- Worker timeout errors in logs
- 502 Proxy Error from Dreamhost
- 500 Internal Server Error
- Works fine when tested in Django shell
- Happens only on wrapper endpoints that self-call

**Quick fix:**
```bash
# Edit gunicorn config
nano deployment/gunicorn_simple.conf.py

# Change workers from 1 to 2 (or more)
workers = 2

# Restart
./deployment/restart_server.sh
```

## Troubleshooting

### Port Already in Use
```bash
# Find what's using the port
lsof -i :8001

# Pick a different port and update:
# 1. gunicorn.conf.py (bind setting)
# 2. Dreamhost Proxy Server configuration
```

### Domain Not Working (404/502 errors)

**Check Proxy Configuration:**
- Go to Dreamhost Panel → Servers → VPS → Proxy Server
- Verify domain is listed and shows "Active"
- Verify port matches your Gunicorn port

**Check Server is Running:**
```bash
lsof -i :8001  # Should show gunicorn processes
./status.sh    # If you have status script
```

**Check Logs:**
```bash
tail -20 ~/your.domain.com/logs/gunicorn_error.log
```

### ALLOWED_HOSTS Error (Bad Request 400)

Add your domain to Django settings.py:
```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.yourdomain.com',
    'YOUR_VPS_IP'
]
```

Restart server after changes.

## Summary Checklist

- [ ] Upload Django project to VPS
- [ ] Create virtualenv and install dependencies
- [ ] Configure Django settings (DEBUG=False, ALLOWED_HOSTS, STATIC_ROOT)
- [ ] Collect static files
- [ ] Choose available port
- [ ] Create and configure Gunicorn
- [ ] Start Gunicorn server
- [ ] **Configure Dreamhost Proxy Server** (Servers → VPS → Proxy Server)
- [ ] Wait for proxy installation to complete
- [ ] Test domain access
- [ ] Set up cron for auto-start
- [ ] Enable SSL (optional)

## Example Ports in Use

Common setup on shared VPS:
- Port 8000: rtah.xyz
- Port 8001: api.pattymdesigns.com
- Port 8888: api.roadtripsandhikes.org

Pick a unique port for each application.
