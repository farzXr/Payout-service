FROM python:3.12

WORKDIR /worker
COPY pyproject.toml ./

RUN pip install poetry && \
    poetry install

CMD ["poetry", "run", "celery", "-A", "core.celery", "worker", "--loglevel=info"]
#CMD ["sleep", "infinity"]