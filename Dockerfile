FROM python:3.10.13-alpine3.18

WORKDIR /app

COPY app/ /app/

RUN pip install -r requirements.txt

CMD [ "/bin/sh", "-c", "alembic upgrade heads && python main.py" ]