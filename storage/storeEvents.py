import pika
import json
import os
from databaseHelper import DBConnection

db_file = os.path.expanduser('~/Telenor/mecs.db')
db_connection = DBConnection(db_file)

def event_insert(event):
    sql_insert = f"""INSERT INTO events (time, node, event, level) VALUES ({event['time']}, '{event['node']}', '{event['event']}', '{event['level']}');"""
    db_connection.execute_statement(sql_insert)

def storeEvent(channel, method, properties, body):
    event = json.loads(body)
    event_insert(event)
    return

#RabbitMQ setup
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='events-out', exchange_type='direct')
channel.queue_declare(queue='out', exclusive=True)
channel.queue_bind(exchange='events-out', queue='out')
channel.basic_consume(queue='out', on_message_callback=storeEvent, auto_ack=True)

channel.start_consuming()