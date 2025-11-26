# Gunicorn configuration file
import multiprocessing

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "/var/log/gunicorn/pmd_api_access.log"
errorlog = "/var/log/gunicorn/pmd_api_error.log"
loglevel = "info"

# Process naming
proc_name = "pmd_api"

# Server mechanics
daemon = False
pidfile = "/var/run/gunicorn/pmd_api.pid"
user = None
group = None
tmp_upload_dir = None

# SSL (if needed, but we'll use Nginx for SSL termination)
# keyfile = None
# certfile = None
