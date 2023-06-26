FROM python:3.9-alpine
ENV PYTHONUNBUFFERED 1
RUN apk add --no-cache libmemcached-dev build-base zlib-dev gcc
RUN pip install pipenv
RUN mkdir /app
COPY /Pipfile* /app/
WORKDIR /app
RUN pipenv install --system
COPY . /app/
RUN chmod +x entrypoint.sh