# Patty M Designs API - VPS Deployment Guide (Generic - Requires Sudo)

⚠️ **NOTE: This guide requires sudo access and is NOT for Dreamhost VPS.**

**For Dreamhost VPS deployment, see: [DREAMHOST_VPS_SETUP.md](DREAMHOST_VPS_SETUP.md)**

This guide will walk you through deploying the Django API to a VPS with full sudo access (nginx, systemd, etc.).

## Prerequisites

- VPS with Ubuntu/Debian (assuming Ubuntu 20.04+)
- SSH access to your VPS
- Domain `api.pattymdesigns.com` pointing to your VPS IP
- MySQL database accessible from VPS

## Step 1: Prepare Your VPS

SSH into your VPS:
```bash
ssh YOUR_VPS_USERNAME@YOUR_VPS_IP
```

Update system packages:
```bash
sudo apt update && sudo apt upgrade -y
```

Install required packages:
```bash
sudo apt install -y python3 python3-pip python3-venv nginx mysql-client libmysqlclient-dev build-essential git
```

## Step 2: Set Up Project Directory

Create project directory:
```bash
mkdir -p ~/pattymdesigns.com
cd ~/pattymdesigns.com
```

Clone or upload your project files:
```bash
# Option 1: Using git (if you have a repo)
git clone YOUR_REPO_URL .

# Option 2: Using scp from your local machine
# (Run this from your local machine, not VPS)
# scp -r /Users/larrymoiola/Code/GitHub/pattymdesigns.com/pmd_editor YOUR_VPS_USERNAME@YOUR_VPS_IP:~/pattymdesigns.com/
```

## Step 3: Set Up Python Virtual Environment

Create virtual environment:
```bash
cd ~/pattymdesigns.com
python3 -m venv venv
source venv/bin/activate
```

Install Python dependencies:
```bash
pip install --upgrade pip
pip install -r pmd_editor/requirements.txt
```

## Step 4: Configure Secrets

Copy the secrets template and edit it:
```bash
cd ~/pattymdesigns.com/pmd_editor
cp deployment/secrets.json.template secrets.json
nano secrets.json
```

Update the following values in `secrets.json`:
- `SECRET_KEY`: Generate a new one with: `python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- `MYSQL_PWD`: Your MySQL password
- `pmd_dev_api_key`: Your development API key
- `pmd_prod_api_key`: Your production API key

Secure the secrets file:
```bash
chmod 600 secrets.json
```

## Step 5: Update Django Settings for Production

Edit `pmd_editor/settings.py`:
```bash
nano pmd_editor/settings.py
```

Make these changes:
1. Set `DEBUG = False`
2. Update `ALLOWED_HOSTS` to include your VPS IP if needed
3. Add `https://pattymdesigns.com` to `CORS_ORIGIN_WHITELIST` (without www)
4. Configure `STATIC_ROOT`:
   ```python
   STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
   ```

## Step 6: Run Django Setup Commands

Collect static files:
```bash
cd ~/pattymdesigns.com/pmd_editor
source ../venv/bin/activate
python manage.py collectstatic --noinput
```

Run migrations (if needed):
```bash
python manage.py migrate
```

Test that Django works:
```bash
python manage.py runserver 0.0.0.0:8000
```
Visit `http://YOUR_VPS_IP:8000` to verify. Press Ctrl+C to stop.

## Step 7: Set Up Gunicorn

Create log directory:
```bash
sudo mkdir -p /var/log/gunicorn
sudo chown $USER:$USER /var/log/gunicorn
```

Create PID directory:
```bash
sudo mkdir -p /var/run/gunicorn
sudo chown $USER:$USER /var/run/gunicorn
```

Test Gunicorn manually:
```bash
cd ~/pattymdesigns.com/pmd_editor
source ../venv/bin/activate
gunicorn --bind 127.0.0.1:8000 pmd_editor.wsgi:application
```
Press Ctrl+C to stop after verifying it works.

## Step 8: Set Up Systemd Service

Edit the service file and update YOUR_VPS_USERNAME:
```bash
cd ~/pattymdesigns.com/pmd_editor/deployment
nano pmd_api.service
# Replace all instances of YOUR_VPS_USERNAME with your actual username
```

Copy service file to systemd:
```bash
sudo cp ~/pattymdesigns.com/pmd_editor/deployment/pmd_api.service /etc/systemd/system/
```

Enable linger for your user (so service runs without being logged in):
```bash
sudo loginctl enable-linger $USER
```

Reload systemd, enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable pmd_api
sudo systemctl start pmd_api
```

Check service status:
```bash
sudo systemctl status pmd_api
```

View logs if there are issues:
```bash
sudo journalctl -u pmd_api -f
```

## Step 9: Configure Nginx

Edit the Nginx config and update YOUR_VPS_USERNAME:
```bash
cd ~/pattymdesigns.com/pmd_editor/deployment
nano nginx.conf
# Replace all instances of YOUR_VPS_USERNAME with your actual username
```

Copy Nginx config (temporarily without SSL):
```bash
sudo cp ~/pattymdesigns.com/pmd_editor/deployment/nginx.conf /etc/nginx/sites-available/pmd_api
```

For now, edit the copied file to comment out SSL lines:
```bash
sudo nano /etc/nginx/sites-available/pmd_api
```

Comment out the SSL server block and just keep HTTP for now:
```nginx
server {
    listen 80;
    server_name api.pattymdesigns.com;

    # Logging
    access_log /var/log/nginx/pmd_api_access.log;
    error_log /var/log/nginx/pmd_api_error.log;

    # Max upload size
    client_max_body_size 10M;

    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/pmd_api /etc/nginx/sites-enabled/
```

Test Nginx configuration:
```bash
sudo nginx -t
```

Restart Nginx:
```bash
sudo systemctl restart nginx
```

Test by visiting: `http://api.pattymdesigns.com`

## Step 10: Set Up SSL with Let's Encrypt

Install Certbot:
```bash
sudo apt install -y certbot python3-certbot-nginx
```

Get SSL certificate:
```bash
sudo certbot --nginx -d api.pattymdesigns.com
```

Certbot will automatically update your Nginx config. Follow the prompts.

Verify SSL renewal:
```bash
sudo certbot renew --dry-run
```

## Step 11: Final Configuration

Now update your Nginx config to use the full SSL version:
```bash
sudo nano /etc/nginx/sites-available/pmd_api
```

Replace with the full SSL config from `deployment/nginx.conf` (the version with both HTTP and HTTPS server blocks).

Restart Nginx:
```bash
sudo systemctl restart nginx
```

## Step 12: Test Your API

Visit: `https://api.pattymdesigns.com`

Test your API endpoints to ensure everything works.

## Maintenance Commands

### Restart the API
```bash
sudo systemctl restart pmd_api
```

### View API logs
```bash
sudo journalctl -u pmd_api -f
```

### View Nginx logs
```bash
sudo tail -f /var/log/nginx/pmd_api_access.log
sudo tail -f /var/log/nginx/pmd_api_error.log
```

### Update code
```bash
cd ~/pattymdesigns.com
# Pull new changes or upload files
source venv/bin/activate
cd pmd_editor
python manage.py collectstatic --noinput
python manage.py migrate
sudo systemctl restart pmd_api
```

## Troubleshooting

### Service won't start
```bash
sudo journalctl -u pmd_api -n 50 --no-pager
```

### Nginx issues
```bash
sudo nginx -t
sudo tail -f /var/log/nginx/error.log
```

### Database connection issues
Check that MySQL host is accessible:
```bash
mysql -h mysql.api.pattymdesigns.com -u pmd_user -p pmd_strings
```

### Permission issues
Ensure correct ownership:
```bash
cd ~/pattymdesigns.com
chown -R $USER:$USER .
```
