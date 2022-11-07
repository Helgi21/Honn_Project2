import pika 
from retry import retry
import yagmail
from dotenv import dotenv_values

env = dotenv_values(".env")
email = env["EMAIL"]
pw = env["PASSWORD"]

class EmailSender:
    def send_email(self, data):    
        yag = yagmail.SMTP(email, pw)
        yag.send(data['email'], data['subject'], data['body'])