FROM python:3.12

WORKDIR /app
COPY pyproject.toml ./

RUN pip install poetry && \
    poetry install

COPY entrypoint.sh /var/bin/entrypoint.sh

RUN chmod +x /var/bin/entrypoint.sh

ENTRYPOINT ["/var/bin/entrypoint.sh"]


CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8080"]