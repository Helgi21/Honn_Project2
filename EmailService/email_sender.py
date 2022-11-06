import pika 
from retry import retry
import yagmail
import requests

class EmailSender:
    def send_email(self, data):    
        yag = yagmail.SMTP("ingolfursibbason@gmail.com", "caqbgjtyrossobtn") #TODO: move email and password to env file
        yag.send(data['email'], data['subject'], data['body'])