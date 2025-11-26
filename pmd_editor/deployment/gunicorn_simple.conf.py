# Gunicorn configuration file (user-space version)
import multiprocessing

# Server socket
bind = "0.0.0.0:8001"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "/home/lar_mo/api.pattymdesigns.com/logs/gunicorn_access.log"
errorlog = "/home/lar_mo/api.pattymdesigns.com/logs/gunicorn_error.log"
loglevel = "info"

# Process naming
proc_name = "pmd_api"

# Server mechanics
daemon = False
pidfile = "/home/lar_mo/api.pattymdesigns.com/logs/gunicorn.pid"
