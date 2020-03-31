import pika
import time
import os

#max number of messages in a queue at any moment
threshold = 10
#time interval for checking the queues (in seconds)
interval = 2

def check_queues():
    ringdump_queue = channel.queue_declare(queue = 'in.ringdump', auto_delete = True)
    fake_queue = channel.queue_declare(queue = 'in.fake', auto_delete = True)
    kibana_queue = channel.queue_declare(queue = 'in.kibana', auto_delete = True)
    out_queue = channel.queue_declare(queue = 'out', durable = True, auto_delete = True)

    ringdump_count = ringdump_queue.method.message_count
    fake_count = fake_queue.method.message_count
    kibana_count = kibana_queue.method.message_count
    out_count = out_queue.method.message_count

    print()
    print(" [x] Ringdump queue: " + str(ringdump_count) + " events... " + ("OK!" if ringdump_count <= threshold else "NOT OK!"))
    print(" [x] Fake queue: " + str(fake_count) + " events... " + ("OK!" if fake_count <= threshold else "NOT OK!"))
    print(" [x] Kibana queue: " + str(kibana_count) + " events... " + ("OK!" if kibana_count <= threshold else "NOT OK!"))
    print(" [x] Out queue: " + str(out_count) + " events... " + ("OK!" if out_count <= threshold else "NOT OK!"))
    print()

    if (ringdump_count > threshold) or (fake_count > threshold) or (kibana_count > threshold):
        print()
        print(" [x] Starting a new gateway...")
        print()
        os.system('python3 ../gateway/gateway.py &')

    if out_count > threshold:
        print()
        print(" [x] Starting a new storage worker...")
        print()
        os.system('python3 ../storage/storeEvents.py &')


#RabbitMQ setup
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

last_check = time.time()

print(" [x] Watching queues, press CTRL + C to cancel...")
try:
    while True:
        if time.time() - last_check > interval:
            check_queues()
            last_check = time.time()
except KeyboardInterrupt:
    pass