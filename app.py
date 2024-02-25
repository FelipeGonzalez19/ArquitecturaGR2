from flask import Flask, jsonify, abort
import pika, os, random

app = Flask(__name__)

# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
randomError = random.randint(0, 1000)

count = 0

params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='arqsub') # Declare a queue
def callback(ch, method, properties, body):
    global count
    count = count + 1


    rand = random.randint(0, 1000)
    if (rand == randomError):
        print('Processed until error: ', count) 
        exit(1)

channel.basic_consume('arqsub',
                          callback,
                          auto_ack=True)

print(' [*] Waiting for messages: (',randomError,')')

try: 
    channel.start_consuming()
except pika.exceptions.ConnectionClosedByBroker as ex:
    print('Processed until connection closed: ', count)
    exit(0)
#for method_frame, properties, body in channel.consume('arqsub'):

    # Display the message parts
    #print(method_frame)
    #print(properties)
    #print(body)

    # Acknowledge the message
    #channel.basic_ack(method_frame.delivery_tag)

    # Escape out of the loop after 10 messages
    #if method_frame.delivery_tag == 10:
     #   break


connection.close()