## How to run?
Make sure tools `docker` and `docker-compose` are installed in your system.

Run 
```
docker-compose up --build
```

After that you should be able to access the webserver at `http://127.0.0.1:8080`.

Swagger docs are available here `http://127.0.0.1:8080/docs`.

## Requirements
The project is written and tested using Python==3.10.13

## Running test db

```bash
docker run -d --name backend-tests \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=password \
-e POSTGRES_DB=db \
-p 5555:5432 \
postgres:14
```

##  Running db for migrations

```bash
docker run -d \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=password \
-e POSTGRES_DB=db \
-p 5556:5432 \
postgres:14

export DB_USER=postgres
export DB_PASSWORD=password
export DB_HOST=127.0.0.1
export DB_PORT=5556
export DB_NAME=db
```
