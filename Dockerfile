FROM python:3.13.6-alpine3.21

WORKDIR /app

COPY app/ /app/

RUN pip install -r requirements.txt

CMD [ "/bin/sh", "-c", "alembic upgrade heads && python main.py" ]