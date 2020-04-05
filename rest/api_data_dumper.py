import requests
import json
from data_dump import data_dump

URL = "http://localhost:5000/addEvent"
URL_CLEANUP = "http://localhost:5000/clear"

def load_data():
    loaded_data = data_dump()
    return loaded_data

def send_data(data):
    # cleanup the API's most recent data
    requests.post(URL_CLEANUP)
    for element in data:
        requests.post(URL, data = json.dumps(element))
        print('[x] Sent Event: ', element)
        
# data = load_data()
data = load_data()
send_data(data)