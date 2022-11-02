import pika
from retry import retry

class InventoryEventListener:
    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def get_connection():
        return pika.BlockingConnection(pika.ConnectionParameters('rabbit'))

    def callback(ch, method, properties, body):
        print(f"Received Message: {body.decode()}")

    def start(self):
        connection = get_connection()
        channel = connection.channel()
        channel.queue_declare(queue='payment)

        channel.basic_consume(
                        queue='lab10_queue',
                        auto_ack=True,
                        on_message_callback=callback)

        channel.start_consuming()