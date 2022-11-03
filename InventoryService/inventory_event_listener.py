import pika
from retry import retry

class InventoryEventListener:
    
    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def get_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters('localhost')) # TODO: remember to change to 'rabbit'

    def callback(ch, method, properties, body):
        print(f"Received Message: {body.decode()}")

    def start(self):
        connection = self.get_connection()
        channel = connection.channel()
        channel.queue_declare(queue='payment')
        print("abababbabbababab")
        channel.basic_consume(
                        queue='payment',
                        auto_ack=True,
                        on_message_callback=self.callback)

        channel.start_consuming()