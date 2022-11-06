import pika
from retry import retry
import json

class PaymentEventSender:
    def __init__(self) -> None:
        self.connection = self.__get_connection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='payment')

    def send_event(self, order, successful: bool):
        message = json.dumps({
            "successful": successful,
            "order": order
        })
        self.channel.basic_publish(
                        exchange='',
                        routing_key='payment',
                        body=message)

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters('localhost')) #TODO: Remember to change to 'rabbit' when containerized