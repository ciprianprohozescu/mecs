import pika
import os
import json
import time

class RingDumpEvents:
    def __init__(self, amqp_url, file_loc):
        #RabbitMQ setup
        print('URL: %s' % (amqp_url,))
        parameters = pika.URLParameters(amqp_url)
        connection = pika.BlockingConnection(parameters)

        self.channel = connection.channel()
        self.channel.exchange_declare(exchange = 'events-in', exchange_type = 'direct')
        self.channel.queue_declare(queue = 'in.ringdump', auto_delete = True)
        self.channel.queue_bind(exchange = 'events-in', queue = 'in.ringdump', routing_key = 'in.ringdump')

        self.file_loc = file_loc


    def message_loop(self):
        """simulate event dispatch using differences in event time"""
        print(" Sending events... press CTRL+C to terminate")
        ringdump = open(self.file_loc, 'r')
        last_event = 0

        # read the file in reverse order
        for line in reversed(ringdump.readlines()):
            event = json.loads(line)

            # wait until next event is set to run, limit to 1 second to prevent elongated quiet periods
            limiter = lambda x, y: (x-y if (x-y < 1) else 1)
            time.sleep(limiter(event['time'], last_event))

            self.channel.basic_publish(exchange = 'events-in', routing_key = 'in.ringdump', body = line)
            print(" [x] Sent event!")

            last_event = event['time']

        print(" Closing connection...")

if __name__ == "__main__":
    amqp_url = os.environ['AMQP_URL'] if 'AMQP_URL' in os.environ else 'http://localhost'
    ringdump_events = RingDumpEvents(amqp_url, 'ringdump.json')
    ringdump_events.message_loop()
