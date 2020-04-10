import pika
import os
import json
import time

class Fake_Event_Data_Gen:
    def __init__(self, file_loc):
        #RabbitMQ setup
        amqp_url = os.environ['AMQP_URL']
        print('URL: %s' % (amqp_url,))
        parameters = pika.URLParameters(amqp_url)
        connection = pika.BlockingConnection(parameters)

        self.channel = connection.channel()
        self.channel.exchange_declare(exchange = 'events-in', exchange_type = 'direct')
        self.channel.queue_declare(queue = 'in.fake', auto_delete = True)
        self.channel.queue_bind(exchange = 'events-in', queue = 'in.fake', routing_key = 'in.fake')

        self.file_loc = file_loc

    def message_loop(self):
        """simulate event dispatch using their time_difs"""
        fakedump = open(self.file_loc, 'r')
        line = fakedump.readline()
        print(" Sending events... press CTRL+C to terminate")
        # just in case, don't want any unexpected invalid data errors
        while line:
            event = json.loads(line)
            
            time_diff =  event.pop('time_dif')
            event['time'] = time.time()
            
            self.channel.basic_publish(exchange = 'events-in', routing_key = 'in.fake', body = json.dumps(event))
            print(" [x] Sent event!")
            time.sleep(time_diff/1000)
            line = fakedump.readline()

if __name__ == "__main__":
    fake_event_data_gen = Fake_Event_Data_Gen('fake_data.json')
    fake_event_data_gen.message_loop()
