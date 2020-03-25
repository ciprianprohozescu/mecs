import pika
import json
import pandas as pd
import numpy as np
import sys
if sys.version_info[0] < 3:
    from BytesIO import BytesIO
else:
    from io import BytesIO
    
class Translator():

    """ Open Connection """
    def __init__(self):
        # Connect to RabbitMQ server
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue = 'in.ringdump', auto_delete = True)
        channel.queue_declare(queue = 'in.kibana') # auto_delete = True
        channel.queue_declare(queue = 'in.fake') # auto_delete = True

        print('[x] Waiting for messages, to cancel press Ctrl + C')

        channel.basic_qos(prefetch_count = 1)

        """ Callback setup """
        channel.basic_consume(queue = 'in.ringdump', on_message_callback = self.callback_ringdump)
        channel.basic_consume(queue = 'in.kibana', on_message_callback = self.callback_kibana)
        channel.basic_consume(queue = 'in.fake', on_message_callback = self.callback_fake)
        channel.start_consuming()

    """ Receives the message and calls for modification """
    def callback_ringdump(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag = method.delivery_tag)
        self.modify_ringdump(body)

    def callback_kibana(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag = method.delivery_tag)
        self.modify_kibana(body)

    def callback_fake(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag = method.delivery_tag)
        self.modify_fake(body)

    """ Ring dump modification - dropping unnecessary attributes """
    # rindgump's attributes are in the same order as in the template
    # deletion of keys should be enough to match UnifiedDataModel
    def modify_ringdump(self, message):
        event = json.loads(message)
        event_template = set(['time',
                              'node',
                              'event',
                              'level'])

        # Remove key, value if not in the template
        for attribute in list(event):
            if not attribute in event_template:
                del event[attribute]

        json_message = json.dump(event)
        self.send(json_message)

    """ Kibana dump modification - renaming, adding labels and dropping unnecessary attributes """
    def modify_kibana(self, message):
        # columns names - for labeling, list of labels that has been renamed:
        # @host -> node, message -> event, @timestamp -> time
        col_names = ['node', '@log_message', 'time', '_id', '_index', '_score',
                    '_type', 'event_timestamp', 'host', 'logsource', 'event',
                    'syslog_facility', 'syslog_facility_code', 'syslog_hostname', 'syslog_pri',
                    'syslog_severity', 'syslog_severity_code', 'syslog_timestamp', 'tags', 'type']

        kibana_line = BytesIO(message)
        # create a dataframe object, it is because I need labels
        df = pd.read_csv(kibana_line, sep = ',', names = col_names)
        # take only the necessary labels and re-arrange them
        df = df.loc[:, ['time', 'node', 'event']]
        # create 'level' column and insert nan value
        df['level'] = np.nan

        json_message = df.to_json(orient = 'records')

        self.send(json_message)
        
    """ Fake dump modification - adding, converting the attributes """
    def modify_fake(self, message):
        event = json.loads(message)
        event['node'] = event['data_center'] + '-' + event['subsection']
        event_template = set(['time', 'node', 'event', 'level'])

        for attribute in list(event):
            if not attribute in event_template:
                del event[attribute]

         # Convert the numerical values to categorical values
        level_template = {1: 'Normal', 2: 'Minor', 3: 'Minor', 4: 'Major' , 5: 'Major' , 6: 'Fatal'}

        event['level'] = level_template[event['level']]

        json_message = json.dumps(event)
        self.send(json_message)

    """  Adds modified json to the queue 'out' """
    def send(self, message):
        connection = pika.BlockingConnection(
                pika.ConnectionParameters(host = 'localhost'))
        channel = connection.channel()

        channel.queue_declare(queue = 'out', durable = True, auto_delete = True)
        print("Sending the events, preess Ctrl + C to cancel")

        channel.basic_publish(exchange = '',
                              routing_key = 'out',
                              body = message,
                              properties = pika.BasicProperties(
                                  delivery_mode = 2, # make message persistent
                              ))
        print(message)
        print("[x] Sent Event")
    
translator = Translator()
