import pika
from retry import retry
from dependency_injector.wiring import inject, Provide
import json

from payment_repository import PaymentRepository
from payment_event_sender import PaymentEventSender
from container import Container


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_connection():
    return pika.BlockingConnection(pika.ConnectionParameters('localhost')) # TODO: remember to change 'localhost' to 'rabbit' when containerized

@inject
def callback(ch, method, properties, body, 
            payment_repository: PaymentRepository = Provide[Container.payment_repository_provider],
            payment_event_sender: PaymentEventSender = Provide[Container.payment_event_sender_provider]):
    body = json.loads(body)
    print(f" Received {body}")
    payment = body['creditCard']
    order_id = body['orderId']
    
    card_is_valid = card_valid(payment)
    print(f"Payment {'successful' if card_is_valid else 'failed'}")
    payment_event_sender.send_event(body, card_is_valid)
    
    return payment_repository.create_payment(order_id, card_is_valid)


# luhn credit card validation
def luhnCheck(ccNum):
    digits = [int(dig) for dig in ccNum]
    evnSum = sum([sum(divmod(2 * d, 10)) for d in digits[-2::-2]])
    oddSum = sum(digits[-1::-2])
    return (oddSum + evnSum) % 10 == 0

def card_valid(card: str) -> bool:
    # Validate card number
    if not luhnCheck(card['cardNumber']):
        print("luhnCheck failed")
        return False
    # Validate card expiration date
    if not 1 <= card['expirationMonth'] <= 12:
        print("expiration_month failed")
        return False
    
    if len(str(card['expirationYear'])) != 4:
        print("expiration_year failed")
        return False
    
    # Validate cvc
    if len(str(card['cvc'])) != 3:
        print("cvc failed")
        return False
    
    return True


if __name__ == '__main__':
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue='paym_order_creation')

    container = Container()
    container.wire(modules=[__name__])

    channel.basic_consume(
                    queue='paym_order_creation',
                    auto_ack=True,
                    on_message_callback=callback)

    channel.start_consuming()
    
