from functools import lru_cache
import pika
from retry import retry
import json

class InventoryEventListener:
    
    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def get_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters('localhost')) # TODO: remember to change to 'rabbit'

    def payment_callback(self, ch, method, properties, body):
        # Updates the product inventory amount if payment successful
        print("received payment event")
        body = json.loads(body)
        with open('../persistance/products.json', 'r+') as f:
            products = json.load(f)
            for product in products:
                if product['productId'] == body['order']['productId']:
                    if body['successful']:
                        product['quantity'] -= body['order']['quantity']
                    product['reserved'] -= body['order']['quantity']
                    print(products)
                    f.seek(0)
                    f.truncate()
                    f.write(json.dumps(products))
                    break
    
    def reserve_callback(self, ch, method, properties, body):
        # reserves the product in the order resceived in the event
        print("received reserve event")
        body = json.loads(body)
        with open('../persistance/products.json', 'r+') as f:
            products = json.load(f)
            for product in products:
                if product['productId'] == body['productId']:
                    product['reserved'] += body['quantity']
                    f.seek(0)
                    f.truncate()
                    f.write(json.dumps(products))
                    break

    def start(self):
        connection = self.get_connection()
        channel = connection.channel()
        channel.queue_declare(queue='order_creation') # Queue with Order-Created events for reserving products
        channel.queue_declare(queue='payment') # Queue with Payment-Success and Payment-Failure events

        print("EventListener: running and waiting for payment and reserve events")
        channel.basic_consume(
            queue='order_creation',
            auto_ack=True,
            on_message_callback=self.reserve_callback
        )

        channel.basic_consume(
            queue='payment',
            auto_ack=True,
            on_message_callback=self.payment_callback
        )
        
        channel.start_consuming()