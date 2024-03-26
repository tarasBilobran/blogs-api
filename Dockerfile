FROM python:3.10-slim

ENV WORKDIR /opt/app
WORKDIR ${WORKDIR}
ENV PYTHONPATH=${PYTHONPATH}:${WORKDIR}

COPY service service/
COPY migrations migrations/
COPY alembic.ini alembic.ini
COPY requirements.txt requirements.txt
COPY entrypoint.sh entrypoint.sh

RUN apt update && apt install -y graphviz graphviz-dev
RUN apt install -y netcat-traditional
RUN pip install -r requirements.txt

ENV PORT=8080 \
  DB_USER="postgres" \
  DB_PASSWORD="password" \
  DB_NAME="db" \
  DB_HOST="db" \
  DB_PORT="5432"

EXPOSE $PORT

ENTRYPOINT sh entrypoint.sh
