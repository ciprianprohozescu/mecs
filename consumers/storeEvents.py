import pika
import json
import os
from databaseHelper import DBConnection

db_file = os.path.expanduser('~/Telenor/mecs.db')
db_connection = DBConnection(db_file)
print(' Connected to database!')

def event_insert(event):
    sql_insert = f"""INSERT INTO events (time, node, event, level) VALUES ({event['time']}, '{event['node']}', '{event['event']}', '{event['level']}');"""
    db_connection.execute_statement(sql_insert)

def storeEvent(channel, method, properties, body):
    event = json.loads(body)
    event_insert(event)
    channel.basic_ack(delivery_tag = method.delivery_tag)
    print('[x] Event stored!')

#RabbitMQ setup
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue = 'out.storage', durable = True, auto_delete = True)

#don't dispatch a message to a consumer until it has acknowledged the previous one
channel.basic_qos(prefetch_count = 1)
channel.basic_consume(queue = 'out.storage', on_message_callback = storeEvent)

print(' Waiting for events... press CTRL+C to terminate')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    pass