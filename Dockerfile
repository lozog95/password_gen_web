FROM python:3.6.5-alpine

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

ENV FLASK_APP password_web

ENV FLASK_RUN_PORT 5000

ENV FLASK_RUN_HOST 0.0.0.0

CMD ["flask", "run"]