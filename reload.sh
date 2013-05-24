#kill -HUP `cat /var/run/gunicorn/imgbbs.pid`
pkill gunicorn
sh ./gunicorn.sh
