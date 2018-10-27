# XTRD API

## Development server

### Build
Run `make build` or `docker-compose build`

### Run application

Run the backend:

```
make start
```

Navigate to `http://localhost:9002/api/docs/`


###CELERY

Run `celery -A app beat -l info`

Run `celery -A app worker -l info`
