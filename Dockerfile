FROM python:3

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /code
COPY ./weather_project/requirements.txt /code/
RUN pip install -r requirements.txt