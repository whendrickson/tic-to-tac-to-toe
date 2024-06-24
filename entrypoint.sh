#!/bin/sh
DATABASE="/home/mine/tictotactotoe/db.sqlite3"
if [ ! -f ${DATABASE} ]; then touch "$DATABASE"; fi
python3 /home/mine/tictotactotoe/manage.py migrate
exec gunicorn --bind 0.0.0.0:8000 --chdir /home/mine/tictotactotoe --reload tictotactotoe.asgi:application --worker-class uvicorn.workers.UvicornWorker
