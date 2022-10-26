ARG APP_ENV=production

FROM python:3.10-slim-bullseye AS base

WORKDIR /opt/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./
RUN pip install -r requirements.txt

FROM base as production-preinstall
# RUN echo "copying necesary files for PROD"
COPY requirements-prod.txt ./
COPY src ./src
RUN  pip install -r requirements-prod.txt

CMD bash -c 'python3 -m uvicorn src.webapi.main:app --host=0.0.0.0 --port=$PORT'

FROM base as development-preinstall
# RUN echo "Installing necesary libs for DEV"
COPY requirements-dev.txt ./
RUN pip install -r requirements-dev.txt
CMD bash

FROM ${APP_ENV}-preinstall as final
