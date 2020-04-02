import flask
from flask import request, jsonify
import pika
import json
import threading

events = []
max_size = 50

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return jsonify(events)

@app.route('/update', methods = ['POST'])
def update():
    global events
    event = json.loads(request.data)
    events.append(event)
    if len(events) > max_size:
        events = events[1:]
    print('[x] Event received!')
    return 'OK'

app.run()