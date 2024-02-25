import pika, os, random

# URL of RabbitMQ
url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
# We generate a random number of requests to make
messagesToSend = random.randint(150, 300)

print('start to send ', messagesToSend)
global count

count = 0

params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='arqsub') # Declare a queue
    
for x in range(messagesToSend):

    channel.basic_publish(exchange='',
                      routing_key='arqsub',
                      body='ALERT'+str(x))
    
    # we count the number of messages that go out
    count = count + 1


print(count, ' messages sent ')
connection.close()
