import pika
from retry import retry


class OrderEventSender:
    def __init__(self) -> None:
        self.connection = self.__get_connection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='order_creation')

    def send_event(self, message):
        self.channel.basic_publish(
                        exchange='',
                        routing_key='order_creation',
                        body=message)

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters('rabbit'))