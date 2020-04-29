import requests
import pika
import json
import os


class postWebEvents:
    def __init__(self):
        self.api_endpoint = os.environ['API_ENDPOINT']
        #RabbitMQ setup
        amqp_url = os.environ['AMQP_URL']
        parameters = pika.URLParameters(amqp_url)
        connection = pika.BlockingConnection(parameters)

        self.channel = connection.channel()
        self.channel.queue_declare(queue = 'out.web', durable = True, auto_delete = True)
        self.channel.basic_consume(queue = 'out.web', on_message_callback = self.postEvent)

        print(' Waiting for events... press CTRL+C to terminate')
        self.channel.start_consuming()

    def postEvent(self, channel, method, properties, body):
        try:
            requests.post(url = self.api_endpoint, data = body)
        except requests.exceptions.RequestException as e:
            print(e)
        self.channel.basic_ack(delivery_tag = method.delivery_tag)
        print('[x] Event posted!')

if __name__ == "__main__":
    postweb = postWebEvents()
