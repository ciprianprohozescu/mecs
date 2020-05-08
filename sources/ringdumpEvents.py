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
ringdump = open('../ringdump.json')
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

#simulate event dispatch using their timestamps
try:
    while True:
        line = ringdump.readline()
        event = json.loads(line)
        while not 'time' in event:
            line = ringdump.readline()
            event = json.loads(line)
        
        time.sleep((float(event['time']) - last_event_theoretical) / 1000)

        last_event_theoretical = float(event['time'])
        channel.basic_publish(exchange = 'events-in', routing_key = 'in.ringdump', body = line)
        print(" [x] Sent event!")
except KeyboardInterrupt:
    pass

print(" Closing connection...")

connection.close()