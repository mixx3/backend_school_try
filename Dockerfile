FROM python:3.10
WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt


ADD gunicorn_conf.py alembic.ini /app/
ADD .env /app/.env
ADD migrations /app/migrations
ADD engine /app/engine

CMD [ "python3", "/app/db_utils.py"]

CMD [ "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "/app/gunicorn_conf.py", "engine.routes.base:app" ]
