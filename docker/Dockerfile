FROM python:3.10-slim-bullseye AS build

RUN apt update -y && apt install -y gcc libssl-dev libcurl4-openssl-dev
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.10-slim-bullseye
RUN apt update -y && apt install -y --no-install-recommends libssl-dev libcurl4-openssl-dev
ENV PATH=/root/.local/bin:$PATH
COPY --from=build /root/.local /root/.local
WORKDIR /app
COPY src/ /app/

CMD [ "gunicorn", "settings.wsgi:application", "-c", "settings/gunicorn_conf.py" ]
