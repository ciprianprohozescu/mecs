# importing the requests library 
import requests 
import pika
import json
from datetime import datetime
import time

class Api_Listener():
    
    def __init__(self):
        pass
    
    def establish_connection(self):
        """ Using Rabbitmq, open a connection and create a queue """
        self.connection = pika.BlockingConnection(
                        pika.ConnectionParameters(host = 'localhost'))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='events-in', exchange_type='direct')
        self.channel.queue_declare(queue = 'in.fake', auto_delete = True)
        self.channel.queue_bind(exchange='events-in', queue='in.fake', routing_key='in.fake')
    
    def receive_data(self):
        """ Sends GET request to the API """
        # sending get request and saving the response as response object 
        response = requests.get("http://localhost:5000/recent")
        # print(response.status_code)
        return response.json()
        
    def listen_for_data(self, data):
        """ Receives any new data from the API """
        self.send(json.dumps(data))
        
    def send_data(self, data):
        """ Pass each serialized dictionary """
        for element in data:
            self.send(json.dumps(element))
    
    def receive_send_data(self):
        """ Combination of receive_data, send_data, running in a loop,
            listens for data every 5 seconds and then sends it """
        while True:
            data = self.receive_data()
            if data:
                self.send_data(data)
            else:
                print('No new data')
            time.sleep(10)

    def send(self, message): 
        """ Publish the message to the queue """
        print("Sending the events, preess Ctrl + C to cancel")
        
        self.channel.basic_publish(exchange = 'events-in',
                              routing_key = 'in.fake',
                              body = message,
        properties = pika.BasicProperties(
            delivery_mode = 2, # make message persistent
        ))
            
        print(message)
        print("[x] Sent Event")

if __name__ == "__main__":  
    apiListener = Api_Listener()
    apiListener.establish_connection()
    apiListener.receive_send_data()
