# Quick Start Deployment Guide (Generic - Requires Sudo)

⚠️ **NOTE: This guide requires sudo access and is NOT for Dreamhost VPS.**

**For Dreamhost VPS deployment, see: [QUICKSTART.md](QUICKSTART.md)**

All files have been uploaded to your VPS. Follow these steps to deploy:

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

Change:
- `DEBUG = False`
- Verify `ALLOWED_HOSTS` includes `.pattymdesigns.com`
- Add to `CORS_ORIGIN_WHITELIST`:
  ```python
  CORS_ORIGIN_WHITELIST = (
      'http://localhost',
      'https://pattymdesigns.com',
      'https://www.pattymdesigns.com',
      'https://www.pattymcmahan.com'
  )
  ```
- Add `STATIC_ROOT`:
  ```python
  STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
  ```

## Step 4: Run Setup Script

This will install system packages, create virtualenv, and install Python dependencies:

```bash
cd /home/lar_mo/api.pattymdesigns.com/pmd_editor
./deployment/setup_vps.sh
```

You'll be prompted for your sudo password.

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

## Step 6: Run Deployment Script

This will set up systemd service, enable linger, and configure Nginx:

```bash
./deployment/deploy.sh
```

## Step 7: Test HTTP Access

Visit: http://api.pattymdesigns.com

You should see your API responding!

## Step 8: Set Up SSL Certificate

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d api.pattymdesigns.com
```

Follow the prompts. Certbot will automatically configure SSL.

## Step 9: Restore Full Nginx Config (if needed)

If you want to use the full SSL config from deployment/nginx.conf:

```bash
sudo cp /home/lar_mo/api.pattymdesigns.com/pmd_editor/deployment/nginx.conf /etc/nginx/sites-available/pmd_api
sudo nginx -t
sudo systemctl restart nginx
```

## Step 10: Test HTTPS Access

Visit: https://api.pattymdesigns.com

## Done! 🎉

Your API is now deployed and running!

## Useful Commands

### View API logs
```bash
sudo journalctl -u pmd_api -f
```

### Restart API
```bash
sudo systemctl restart pmd_api
```

### Check API status
```bash
sudo systemctl status pmd_api
```

### Update code after changes
```bash
cd /home/lar_mo/api.pattymdesigns.com
source venv/bin/activate
cd pmd_editor
git pull  # or upload new files
python manage.py collectstatic --noinput
python manage.py migrate
sudo systemctl restart pmd_api
```

## Troubleshooting

### Service won't start
```bash
sudo journalctl -u pmd_api -n 50 --no-pager
```

### Check Gunicorn logs
```bash
sudo tail -f /var/log/gunicorn/pmd_api_error.log
```

### Check Nginx logs
```bash
sudo tail -f /var/log/nginx/pmd_api_error.log
```

### Test database connection
```bash
mysql -h mysql.api.pattymdesigns.com -u pmd_user -p pmd_strings
```
