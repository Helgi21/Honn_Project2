import pika
from retry import retry
from dependency_injector.wiring import inject, Provide
import json
import yagmail
import requests

from email_sender import EmailSender
from container import Container


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_connection():
    return pika.BlockingConnection(pika.ConnectionParameters('localhost')) #TODO: remember to change to 'rabbit' when running in docker

def get_email_addresses(order):
    merchant = requests.get(f'http://localhost:8001/merchants/{order["merchantId"]}')
    buyer = requests.get(f'http://localhost:8002/buyers/{order["buyerId"]}')
    print(merchant["email"], buyer["email"])
    return {
        "merchantEmail": 'helgi203@gmail.com', # merchant["email"],
        "buyerEmail": 'ingolfusibbason@gmail.com' #buyer["email"]
    }

@inject
def order_callback(ch, method, properties, body,
            email_sender: EmailSender = Provide[Container.email_sender_provider]):
    data = json.loads(body)
    print(f" Received order event {data}")

    product = requests.get('http://localhost:8000/products/{}'.format(data['product_id']))
    email_adr = get_email_addresses(data)
    email_data = {
        "email": [email_adr["merchantEmail"], email_adr["buyerEmail"]],
        "subject": "Order has been created",
        "body": {'id': data['id'], 'product_name': product['productName'], 'price': product['price']}
    }

    email_sender.send_email(email_data)


@inject
def payment_callback(ch, method, properties, body,
            email_sender: EmailSender = Provide[Container.email_sender_provider]):
    data = json.loads(body)
    print(f" Received payment event {data}")
    payment_success = data['successful']
    email_adr = get_email_addresses(data)

    if payment_success:
        email_data = {
            "email": [email_adr["merchantEmail"], email_adr["buyerEmail"]],
            "subject": "Order has been purchased",
            "body": f"Order {data['id']} has been successfully purchased"
        }
    else:
        email_data = {
            "email": [email_adr["merchantEmail"], email_adr["buyerEmail"]],
            "subject": "Order purchase failed",
            "body": f"Order {data['id']} purchase has failed"
        }
    
    email_sender.send_email(email_data)    
    
    
if __name__ == '__main__':
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue='email_order_creation')
    channel.queue_declare(queue='email_payment')
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

    email = "ingolfursibbason@gmail.com"
    subject = "Test"
    content = "This is a test"
    yag = yagmail.SMTP("honn.project2@gmail.com", "Hunter.2") #TODO: move email and password to env file
    yag.send(email, subject, content)
    
    channel.start_consuming()