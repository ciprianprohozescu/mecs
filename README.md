# mecs
Massive Event Correlation System

How to set up the non-Docker system:
- Prerequisites: RabbitMQ, Python 3 (packages: sqlite3, pika, pandas, numpy, flask), NPM.
- Checkout the *development* branch
- Go to this link https://ucndk-my.sharepoint.com/:f:/g/personal/1074220_ucn_dk/EvqMEWsenkZBrtd3PlsOXmkBMmqUWVRY7QTJH3zVtSmqsg?e=kjyRQv and download the 3 data files in your *mecs* directory. The 3 files must be in the root directory, not in a subfolder.
- Start up the RabbitMQ broker by running *rabbitmq-server*.
- Set up the database by running *databaseSetup.py*.
- To set up the web client, run *npm install* in the *web-mecs* directory.
- To run the web client, *npm run serve* in the *web-mecs* directory.
- Run the *webApi.py* script to allow the web client to receive data.
- Run the consumers: *storeEvents.py* *webConsumer.py*.
- Run the gateway: *gateway.py*.
- Run the sources (at least one to see data): *fakeEvents.py* *kibanaEvents.py* *ringdumpEvents.py*.
