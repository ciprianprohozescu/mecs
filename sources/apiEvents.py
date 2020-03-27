# importing the requests library 
import requests 
import pika
import json

class Api_Listener():
    
    def __init__(self):
        pass
    
    def receive_data(self):
        """ Sends GET request to the API """
        # sending get request and saving the response as response object 
        response = requests.get("http://localhost:5000/all")
        # print(response.status_code)
        return response.json()
    
    def send_data(self, data):
        """ Pass each serialized dictionary """
        for element in data:
            self.send(json.dumps(element))

    def send(self, message): 
        """ Using Rabbitmq, open a connection, create a queue and send the data """
        connection = pika.BlockingConnection(
                        pika.ConnectionParameters(host = 'localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='events-in', exchange_type='direct')
        channel.queue_declare(queue = 'in.fake', auto_delete = True)
        channel.queue_bind(exchange='events-in', queue='in.fake', routing_key='in.fake')

        print("Sending the events, preess Ctrl + C to cancel")
        
        channel.basic_publish(exchange = 'events-in',
                              routing_key = 'in.fake',
                              body = message,
        properties = pika.BasicProperties(
            delivery_mode = 2, # make message persistent
        ))
            
        print(message)
        print("[x] Sent Event")

api_listener = Api_Listener()
data = api_listener.receive_data()
api_listener.send_data(data)