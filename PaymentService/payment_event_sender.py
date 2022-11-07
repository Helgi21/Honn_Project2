import pika
from retry import retry
import json

class PaymentEventSender:
    def __init__(self) -> None:
        self.connection = self.__get_connection()
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='payment_exchange', exchange_type='fanout')

        q1 = self.channel.queue_declare(queue='email_payment', durable=True)
        q2 = self.channel.queue_declare(queue='inv_payment', durable=True)
        
        self.channel.queue_bind(exchange='payment_exchange', queue=q1.method.queue)
        self.channel.queue_bind(exchange='payment_exchange', queue=q2.method.queue)
    def send_event(self, order, successful: bool):
        message = json.dumps({
            "successful": successful,
            "order": order
        })
        self.channel.basic_publish(
                        exchange='payment_exchange',
                        routing_key='',
                        body=message)
        

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters('rabbit', heartbeat=0))