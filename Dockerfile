FROM python:2.7

RUN pip install flask psycopg2

COPY . /app

WORKDIR /app

ENV TABKEEPER_ENV production

CMD python app.py
