# PROD

# pull official base image
FROM python:3.10.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
  curl \
  postgresql-client \
  && rm -rf /var/lib/apt/lists/*


RUN useradd -r -s /bin/bash alex

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONFAULTHANDLER 1

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt
# EXPOSE 80

#USER alex
COPY --chown=alex:alex ./migrations /src/migrations
COPY --chown=alex:alex ./alembic.ini /src/alembic.ini
COPY --chown=alex:alex ./app /src/app


WORKDIR /src

# EXPOSE 80

# ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000" "--reload", "--debug"]
# CMD uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload --debug --reload-dir /src/app
# CMD uvicorn app.main:app --host 0.0.0.0 --port 5000 
CMD ["uvicorn", "app.main:app","--no-server-header","--no-proxy-headers", "--host", "0.0.0.0", "--port", "5000" ]

# ENTRYPOINT ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", ":5000", "app.main:app"]


HEALTHCHECK --interval=21s --timeout=3s --start-period=10s CMD curl --fail http://localhost:5000/health || exit 1

# EXPOSE 5432