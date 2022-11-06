import pika
from retry import retry


class OrderEventSender:
    def __init__(self) -> None:
        self.connection = self.__get_connection()
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='order_creation',
                        exchange_type='fanout')

        queue1 = self.channel.queue_declare(queue='inv_order_creation')
        queue2 = self.channel.queue_declare(queue='paym_order_creation')
        self.channel.queue_bind(exchange='order_creation',
                    queue=queue1.method.queue)
        self.channel.queue_bind(exchange='order_creation',
                    queue=queue2.method.queue)

    def send_event(self, message):
        # Publishing to the order_creation exchange instead of a single queue
        self.channel.basic_publish(
                        exchange='order_creation',
                        routing_key='',
                        body=message)

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters('rabbit'))