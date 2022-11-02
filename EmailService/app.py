import pika
from retry import retry
from dependency_injector.wiring import inject, Provide
import json
import yagmail

from email_repository import EmailtRepository
from email_event_sender import EmailEventSender
from container import Container


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_connection():
    return pika.BlockingConnection

def send_mail(email, subject, content):
    yag = yagmail.SMTP("honn.project2@gmail.com", "Hunter.2")