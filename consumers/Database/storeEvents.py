import pika
import json
import os
from databaseSetup import DatabaseSetup
from databaseHelper import DBConnection

class StoreEvents:
    def __init__(self, db_loc):
        self.db_connection = DBConnection(db_loc)
        print(' Connected to database!')

        #RabbitMQ setup
        amqp_url = os.environ['AMQP_URL']
        parameters = pika.URLParameters(amqp_url)
        connection = pika.BlockingConnection(parameters)

        channel = connection.channel()
        channel.queue_declare(queue = 'out.storage', durable = True, auto_delete = True)
        channel.basic_consume(queue = 'out.storage', on_message_callback = self.storeEvent)

        print(' Waiting for events... press CTRL+C to terminate')
        channel.start_consuming()

    def event_insert(self, event):
        sql_insert = f"""INSERT INTO events (time, node, event, level) VALUES 
        ({event['time']}, '{event['node']}', '{event['event']}', '{event['level']}');"""
        self.db_connection.execute_statement(sql_insert)

    def storeEvent(self, channel, method, properties, body):
        event = json.loads(body)
        self.event_insert(event)
        channel.basic_ack(delivery_tag = method.delivery_tag)
        print('[x] Event stored!')


if __name__ == "__main__":
    db_loc = os.environ['SQLITE_DB_LOC']

    if not os.path.exists(db_loc):
        dbsetup = DatabaseSetup(db_loc)
        print('creating new database')
        dbsetup.setup()

    store_events = StoreEvents(db_loc)
