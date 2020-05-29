FROM python:3

RUN pip install pika

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
COPY gateway.py .

CMD ["python3", "/usr/src/app/gateway.py"]
