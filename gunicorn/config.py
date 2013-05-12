## Server Socket
# bind = '127.0.0.1:xxxxx'
# bind = 'xx.xx.xx.xx:xxxxx'
bind = 'unix:/tmp/gunicorn_imgbbs.sock'

backlog = 2048

## Worker Processes
workers = 1
worker_class = 'sync'
worker_connections = 1000
max_requests = 0
timeout = 30
keepalive = 2

debug = True
spew  = False

## Server Mechanics
preload_app = True
daemon = True
pidfile = '/var/run/gunicorn/imgbbs.pid' # 起動前に/var/run/gunicornを作成する
user  = 'ubuntu'
group = 'ubuntu'
#umask = 0002

## Logging
logfile = '/var/log/gunicorn/imgbbs.log' # 起動前に/var/log/gunicornを作成する
loglevel = 'info'
logconfig = None

## Process Naming
proc_name = 'gunicorn_imgbbs'
