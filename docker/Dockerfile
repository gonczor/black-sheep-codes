FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ /app/

CMD [ "gunicorn", "settings.wsgi:application", "-c", "settings/gunicorn_conf.py" ]
