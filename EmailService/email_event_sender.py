import pika 
from retry import retry

class EmailEventSender:
    def __init__(self) -> None:
        self.connection = self.__get_connection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='email_queue')
    
    def send_event(self, message):
        self.channel.basic_publish(
                        exchange='',
                        routing_key='email_queue',
                        body=message)

    retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters('rabbit'))