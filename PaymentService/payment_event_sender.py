import pika
from retry import retry


class PaymentEventSender:
    def __init__(self) -> None:
        self.connection = self.__get_connection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='payment_success_queue')
        self.channel.queue_declare(queue='payment_failure_queue')

    def send_event(self, message, successful):
        queue = "payment_success_queue" if successful else "payment_failure_queue"
        self.channel.basic_publish(
                        exchange='',
                        routing_key=queue,
                        body=message)

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters('rabbit'))