import pika
from retry import retry
from dependency_injector.wiring import inject, Provide
import json

from payment_repository import PaymentRepository
from payment_event_sender import PaymentEventSender
from container import Container


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_connection():
    return pika.BlockingConnection(pika.ConnectionParameters('rabbit'))

@inject
def callback(ch, method, properties, body, 
            payment_repository: PaymentRepository = Provide[Container.payment_repository_provider],
            payment_event_sender: PaymentEventSender = Provide[Container.payment_event_sender_provider]):
    print(f" Received {body}")
    payment = json.loads(body)['creditCard']
    order_id = json.loads(body)['id']
    
    card_is_valid = card_valid(payment)
    print(f"Payment {'successful' if card_is_valid else 'failed'}")
    payment_event_sender.send_event(body, card_is_valid)
    
    return payment_repository.create_payment(order_id, card_is_valid)


# luhn credit card validation
def luhnCheck(ccNum):
    nDigits = len(ccNum)
    nSum = 0
    isSecond = False
    
    for i in range(nDigits - 1, -1, -1):
        d = ord(ccNum[i]) - ord('0')
        
        if (isSecond == True):
            d = d * 2
        
        # We add two digits to handle
        # cases that make two digits after
        # doubling
        nSum += d // 10
        nSum += d % 10
        
        isSecond = not isSecond
        
        if (nSum % 10 == 0):
            return True
        else:
            return False

def card_valid(card: str) -> bool:
    luhnCheck(card)
    
    # Validate card number
    if not luhnCheck(card['cardNumber']):
        return False
    # Validate card expiration date
    if 1 <= card['expiration_month'] <= 12:
        return False
    
    if len(card['expiration_year']) != 4:
        return False
    
    # Validate cvc
    if len(card['cvc']) != 3:
        return False
    
    return True


if __name__ == '__main__':
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue='order_creation_queue')

    channel.basic_consume(
                    queue='order_creation_queue',
                    auto_ack=True,
                    on_message_callback=callback)

    channel.start_consuming()
    
