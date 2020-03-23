import pika
import os
import json
import time

#RabbitMQ setup
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='events', exchange_type='direct')
channel.queue_declare(queue='in.fake')
channel.queue_bind(exchange='events', queue='in.fake')

#open the fake dump
fakedump = open(os.path.expanduser('~/Telenor/fake_data.json'))
print(" Sending events... press CTRL+C to terminate")

#assign a timestamp to the first event
last_event = time.time()

#simulate event dispatch using their time_difs
try:
    while True:
        line = fakedump.readline()
        event = json.loads(line)
        
        try:
            while event['time_dif'] > 1000 * (time.time() - last_event):
                continue
        except KeyboardInterrupt:
            break

        channel.basic_publish(exchange='events', routing_key='in.fake', body=line)
        print(" [x] Sent event!")
        last_event = time.time()
except KeyboardInterrupt:
    pass

print(" Closing connection...")

connection.close()