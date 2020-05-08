import pika
import os
import json
import time

#RabbitMQ setup
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange = 'events-in', exchange_type = 'direct')
channel.queue_declare(queue = 'in.fake', auto_delete = True)
channel.queue_bind(exchange = 'events-in', queue = 'in.fake', routing_key = 'in.fake')

#open the fake dump
fakedump = open('../fake_data.json')
print(" Sending events... press CTRL+C to terminate")

#simulate event dispatch using their time_difs
try:
    while True:
        line = fakedump.readline()
        event = json.loads(line)

        time.sleep(event['time_dif'] / 1000)

        del event['time_dif']
        event['time'] = time.time()
        
        channel.basic_publish(exchange = 'events-in', routing_key = 'in.fake', body = json.dumps(event))
        print(" [x] Sent event!")
except KeyboardInterrupt:
    pass

print(" Closing connection...")

connection.close()