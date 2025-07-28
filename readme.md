
 gunicorn wsgi:application -b 0.0.0.0:5001 --timeout 120 --workers 4 --log-file gunicorn.log --access-logfile access.log
