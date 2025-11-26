# Quick Start Deployment Guide (Dreamhost VPS)

All files have been uploaded to your VPS. This guide is for managed VPS without sudo access.

## Step 1: SSH into your VPS

```bash
ssh dhvps
cd /home/lar_mo/api.pattymdesigns.com/pmd_editor
```

## Step 2: Configure Production Secrets

Generate a new Django secret key and update secrets.json:

```bash
# Generate a new secret key
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Edit secrets.json
nano secrets.json
```

Update these values:
- `SECRET_KEY`: Use the generated key above
- Verify `MYSQL_HOST`, `MYSQL_DB`, `MYSQL_USER`, `MYSQL_PWD` are correct
- Update API keys if needed

## Step 3: Update Django Settings for Production

```bash
nano pmd_editor/settings.py
```

Make these changes:

1. Set `DEBUG = False`

2. Verify `ALLOWED_HOSTS`:
```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.pattymdesigns.com', '.pattymcmahan.com', 'YOUR_VPS_IP']
```

3. Update `CORS_ORIGIN_WHITELIST`:
```python
CORS_ORIGIN_WHITELIST = (
    'http://localhost',
    'https://pattymdesigns.com',
    'https://www.pattymdesigns.com',
    'https://www.pattymcmahan.com'
)
```

4. Add `STATIC_ROOT` (add this near the bottom):
```python
import os
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
```

## Step 4: Run Setup Script

This will create virtualenv and install dependencies:

```bash
cd /home/lar_mo/api.pattymdesigns.com/pmd_editor
chmod +x deployment/*.sh
./deployment/setup_vps.sh
```

## Step 5: Test Database Connection

```bash
source /home/lar_mo/api.pattymdesigns.com/venv/bin/activate
cd /home/lar_mo/api.pattymdesigns.com/pmd_editor
python manage.py check
```

If successful, run migrations (if needed):

```bash
python manage.py migrate
```

## Step 6: Start the Server

```bash
./deployment/start_server.sh
```

The server will run on port 8000.

## Step 7: Test Your API

Find your VPS IP address:
```bash
hostname -I
```

Test locally first:
```bash
curl http://localhost:8000
```

Or from your local machine:
```bash
curl http://YOUR_VPS_IP:8000
```

## Step 8: Configure Dreamhost Proxy Server ⚠️ CRITICAL STEP

**This is the key step that connects your domain to your running application!**

1. Log into **Dreamhost Panel**
2. Go to: **Servers → VPS → Proxy Server**
3. Click **"Add Proxy Server"**
4. Configure:
   - **Domain**: `api.pattymdesigns.com`
   - **Port**: `8001` (or your chosen port)
5. Click **"Add Proxy Now"**
6. Wait for installation to complete (5-15 minutes)

Once complete, your API will be accessible at `https://api.pattymdesigns.com`

SSL is automatically provided by Dreamhost.

## Done! 🎉

Your API is now running!

## Useful Commands

### Check server status
```bash
./deployment/status.sh
```

### Stop server
```bash
./deployment/stop_server.sh
```

### Restart server
```bash
./deployment/restart_server.sh
```

### View logs
```bash
# Access log
tail -f ~/api.pattymdesigns.com/logs/gunicorn_access.log

# Error log
tail -f ~/api.pattymdesigns.com/logs/gunicorn_error.log

# Startup log
tail -f ~/api.pattymdesigns.com/logs/nohup.log
```

### Update code after changes
```bash
cd /home/lar_mo/api.pattymdesigns.com
source venv/bin/activate
cd pmd_editor
# Upload new files or git pull
python manage.py collectstatic --noinput
python manage.py migrate
./deployment/restart_server.sh
```

## Troubleshooting

### Server won't start

Check the logs:
```bash
cat ~/api.pattymdesigns.com/logs/nohup.log
tail -20 ~/api.pattymdesigns.com/logs/gunicorn_error.log
```

### Database connection issues

Test database connection:
```bash
mysql -h mysql.api.pattymdesigns.com -u pmd_user -p pmd_strings
```

### Port already in use

Check what's running on port 8000:
```bash
lsof -i :8000
netstat -tulpn | grep 8000
```

### Make server start on boot

Add to your crontab:
```bash
crontab -e
```

Add this line:
```
@reboot /home/lar_mo/api.pattymdesigns.com/pmd_editor/deployment/start_server.sh
```

## Next Steps

For production, you'll want to:
1. Set up proper domain routing through Dreamhost panel
2. Enable SSL/HTTPS
3. Configure firewall rules if available
4. Set up monitoring/alerts
