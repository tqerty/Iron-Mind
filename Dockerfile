FROM python:3.13-slim

WORKDIR /srv

COPY . /srv

RUN pip install -r requirements.txt

ENV PYTHONPATH=/srv

CMD ["gunicorn", "-b", "0.0.0.0:999", "wsgi:app"]