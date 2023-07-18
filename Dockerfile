FROM python:3.7.3
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /app
WORKDIR /app
COPY . /app/

RUN mkdir -p /app/media
RUN mkdir -p /app/static


RUN pip install -r requirements.txt


EXPOSE 8000
ENV LC_ALL=en_US.UTF8
