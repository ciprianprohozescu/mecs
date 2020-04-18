import pika
import os
import json
import time

class KibanaEvents:
    def __init__(self, file_loc):
        #RabbitMQ setup
        amqp_url = os.environ['AMQP_URL']
        print('URL: %s' % (amqp_url,))
        parameters = pika.URLParameters(amqp_url)
        connection = pika.BlockingConnection(parameters)

        self.channel = connection.channel()
        self.channel.exchange_declare(exchange = 'events-in', exchange_type = 'direct')
        self.channel.queue_declare(queue = 'in.kibana', auto_delete = True)
        self.channel.queue_bind(exchange = 'events-in', queue = 'in.kibana', routing_key = 'in.kibana')

        self.file_loc = file_loc
        # time between events being fired out
        self.interval = 1 

    def message_loop(self):
        """simulate event dispatch using their timestamps"""
        #open kibana dump
        ringdump = open(self.file_loc)
        line = ringdump.readline() # skip the first line

        while line:
            print(" Sending events... press CTRL+C to terminate")
            line = ringdump.readline()
            
                #while time.time() - last_event < interval:

            self.channel.basic_publish(exchange = 'events-in', routing_key = 'in.kibana', body = line)
            print(" [x] Sent event!") 
            time.sleep(self.interval)

        print(" Closing connection...")
        connection.close()

if __name__ == "__main__":
    kibana_events = KibanaEvents('errors_last_3_hours.csv')
    kibana_events.message_loop()
