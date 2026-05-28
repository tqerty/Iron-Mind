FROM python:3.13-slim

WORKDIR /srv

COPY . /srv

RUN pip install -r requirements.txt

ENV PYTHONPATH=/srv
ENV GUNICORN_CMD_ARGS="--workers=2 --threads=4 --timeout=120 --graceful-timeout=30 --keep-alive=5 --access-logfile=- --error-logfile=-"

CMD ["gunicorn", "-b", "0.0.0.0:999", "wsgi:app"]
