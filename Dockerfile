FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_DB_PATH=/data/db.sqlite3

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Settings require these variables; their values don't matter for collectstatic.
RUN DJANGO_SECRET_KEY=build DJANGO_ALLOWED_HOSTS=localhost DJANGO_ADMIN_URL=build \
    python manage.py collectstatic --noinput

RUN useradd --uid 1000 --no-create-home app && mkdir /data && chown app /data
USER app

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py createcachetable && exec gunicorn config.wsgi --bind 0.0.0.0:8000 --workers 3 --access-logfile - --no-control-socket"]
