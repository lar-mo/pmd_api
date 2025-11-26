# Deployment Documentation

This folder contains deployment scripts and guides for the Patty M Designs API.

## 📚 Documentation

### For Dreamhost VPS (Primary)
- **[QUICKSTART.md](QUICKSTART.md)** - Quick deployment steps for Dreamhost VPS
- **[DREAMHOST_VPS_SETUP.md](DREAMHOST_VPS_SETUP.md)** - Complete Dreamhost deployment guide

### For Generic VPS with Sudo Access (Reference)
- **[QUICKSTART_GENERIC.md](QUICKSTART_GENERIC.md)** - Quick steps (requires sudo)
- **[DEPLOYMENT_GUIDE_GENERIC.md](DEPLOYMENT_GUIDE_GENERIC.md)** - Full guide (requires sudo, nginx, systemd)

## 🚀 Quick Start

**Using Dreamhost VPS?** → See [QUICKSTART.md](QUICKSTART.md)

**Using other VPS with sudo?** → See [QUICKSTART_GENERIC.md](QUICKSTART_GENERIC.md)

## 📝 Scripts

### Dreamhost VPS (No Sudo)
- `setup_vps.sh` - Install dependencies and set up environment
- `start_server.sh` - Start Gunicorn server
- `stop_server.sh` - Stop Gunicorn server
- `restart_server.sh` - Restart Gunicorn server
- `status.sh` - Check server status and view logs
- `deploy.sh` - Run deployment process

### Configuration Files
- `gunicorn_simple.conf.py` - Gunicorn configuration (Dreamhost)
- `secrets.json.template` - Template for secrets file (DO NOT commit actual secrets.json)

### Generic VPS (Sudo Required - Reference)
- `gunicorn.conf.py` - Gunicorn configuration with system paths
- `pmd_api.service` - Systemd service file
- `nginx.conf` - Nginx reverse proxy configuration

## ⚠️ Important Notes

1. **Never commit `secrets.json`** - It's in .gitignore for a reason
2. **Dreamhost VPS** - Use the non-"generic" guides and scripts
3. **Path references** (like `/home/lar_mo/`) are not secrets - they're useless without server access
4. **Critical step for Dreamhost**: Configure Proxy Server in Dreamhost Panel (see DREAMHOST_VPS_SETUP.md Part 3)
