from flask import Flask, jsonify, abort
import pika, os, random

app = Flask(__name__)


url = os.environ.get("CLOUDAMQP_URL", "amqp://guest:guest@localhost:5672/%2f")
randomError = random.randint(0, 1000)

count = 0

params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue="arqsub")


def callback(ch, method, properties, body):
    global count
    count = count + 1

    rand = random.randint(0, 1000)
    if rand == randomError:
        print("Processed until error: ", count)
        exit(1)


channel.basic_consume("arqsub", callback, auto_ack=True)

print(" [*] Waiting for messages: (", randomError, ")")

try:
    channel.start_consuming()
except pika.exceptions.ConnectionClosedByBroker as ex:
    print("Processed until connection closed: ", count)
    exit(0)

connection.close()
