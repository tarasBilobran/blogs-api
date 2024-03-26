FROM python:3.10-slim

ENV WORKDIR /opt/app
WORKDIR ${WORKDIR}
ENV PYTHONPATH=${PYTHONPATH}:${WORKDIR}

COPY service service/
COPY migrations migrations/
COPY alembic.ini alembic.ini
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ENV PORT=8080 \
  DB_USER="postgres" \
  DB_PASSWORD="password" \
  DB_NAME="db" \
  DB_HOST="db" \
  DB_PORT="5432"

EXPOSE $PORT

ENTRYPOINT alembic upgrade head && gunicorn \
    -k uvicorn.workers.UvicornWorker \
    -b :$PORT service.app:APP
