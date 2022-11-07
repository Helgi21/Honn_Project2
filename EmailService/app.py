import pika
from retry import retry
from dependency_injector.wiring import inject, Provide
import json
import requests

from email_sender import EmailSender
from container import Container


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_connection():
    return pika.BlockingConnection(pika.ConnectionParameters('rabbit'))

def get_email_addresses(order):
    merchant = requests.get(f'http://merchant_service:8001/merchants/{order["merchantId"]}').json()
    buyer = requests.get(f'http://buyer_service:8002/buyers/{order["buyerId"]}').json()
    return {
        "merchantEmail": merchant["email"],
        "buyerEmail": buyer["email"]
    }

@inject
def order_callback(ch, method, properties, body,
            email_sender: EmailSender = Provide[Container.email_sender_provider]):
    data = json.loads(body)
    print(f" Received order event {data}")

    product = requests.get(f'http://inventory_service:8004/products/{data["productId"]}').json()
    email_adr = get_email_addresses(data)
    email_data = {
        "email": [email_adr["merchantEmail"], email_adr["buyerEmail"]],
        "subject": "Order has been created",
        "body": {'id': data['productId'], 'product_name': product['productName'], 'price': product['price']}
    }

    email_sender.send_email(email_data)

@inject
def payment_callback(ch, method, properties, body,
            email_sender: EmailSender = Provide[Container.email_sender_provider]):
    data = json.loads(body)
    print(f" Received payment event {data}")
    payment_success = data['successful']
    email_adr = get_email_addresses(data['order'])

    if payment_success:
        email_data = {
            "email": [email_adr["merchantEmail"], email_adr["buyerEmail"]],
            "subject": "Order has been purchased",
            "body": f"Order {data['order']['orderId']} has been successfully purchased"
        }
    else:
        email_data = {
            "email": [email_adr["merchantEmail"], email_adr["buyerEmail"]],
            "subject": "Order purchase failed",
            "body": f"Order {data['order']['orderId']} purchase has failed"
        }
    
    email_sender.send_email(email_data)    
    
    
if __name__ == '__main__':
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue='email_order_creation')
    channel.queue_declare(queue='email_payment', durable=True)
    container = Container()
    container.wire(modules=[__name__])

    channel.basic_consume(
        queue = 'email_order_creation',
        auto_ack = True,
        on_message_callback = order_callback
    )

    channel.basic_consume(
        queue = 'email_payment',
        auto_ack = True,
        on_message_callback = payment_callback
    )
    channel.start_consuming()