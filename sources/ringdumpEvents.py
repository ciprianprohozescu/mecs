import pika
import os
import json
import time

#RabbitMQ setup
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange = 'events-in', exchange_type = 'direct')
channel.queue_declare(queue = 'in.ringdump', auto_delete = True)
channel.queue_bind(exchange = 'events-in', queue = 'in.ringdump', routing_key = 'in.ringdump')

#open ringdump
ringdump = open(os.path.expanduser('~/Telenor/ringdump.json'))
print(" Sending events... press CTRL+C to terminate")

#read the first event to set the initial time
line = ringdump.readline()
event = json.loads(line)
while not 'time' in event:
    line = ringdump.readline()
    event = json.loads(line)

last_event_theoretical = float(event['time'])
channel.basic_publish(exchange='events-in', routing_key='in.ringdump', body=line)
print(" [x] Sent event!")
last_event_actual = float(time.time())

#simulate event dispatch using their timestamps
try:
    while True:
        line = ringdump.readline()
        event = json.loads(line)
        while not 'time' in event:
            line = ringdump.readline()
            event = json.loads(line)
        
        try:
            while (float(event['time']) - last_event_theoretical) > 1000 * (time.time() - last_event_actual):
                continue
        except KeyboardInterrupt:
            break

        last_event_theoretical = float(event['time'])
        channel.basic_publish(exchange = 'events-in', routing_key = 'in.ringdump', body = line)
        print(" [x] Sent event!")
        last_event_actual = time.time()
except KeyboardInterrupt:
    pass

print(" Closing connection...")

connection.close()