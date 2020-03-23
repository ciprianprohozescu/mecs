import pika
import json

class Translator():

    """ Open Connection """
    def __init__(self):
        # Connect to RabbitMQ server
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue = 'in.ringdump', auto_delete = True)
        print('[x] Waiting for messages, to cancel press Ctrl + C')

        channel.basic_qos(prefetch_count = 1)
        channel.basic_consume(queue = 'in.ringdump', on_message_callback = callback)
        channel.start_consuming()

    """ Receives the message and calls for modification """
    def callback(ch, method, properties, body):
        ch.basic_ack(delivery_tag = method.delivery_tag))
        modify(body)

    """ The template is applied to the json string """
    def modify(message):
        event = json.loads(message)
        event_template = set(['time',
                              'node',
                              'event',
                              'level'])

        # Remove key, value if not in the template
        for attribute in event.keys():
            if not attribue in event_template:
                del event[attribute]

        send(message)

    """  Adds modified json to the queue """
    def send(message):
        connection = pika.BlockingConnection(
                pika.ConnectionParameters(host = 'localhost'))
        channel = connection.channel()

        channel.queue_declare(queue = 'out.ringdump', durable = True, auto_delete = True)
        print("Sending the events, preess Ctrl + C to cancel")

        channel.basic_publish(exchange = '',
                              routing_key = 'out.ringdump',
                              body = message,
                              properties = pika.BasicProperties(
                                  delivery_mode = 2, # make message persistent
                              )
        print("[x] Done")