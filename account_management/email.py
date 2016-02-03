from flask.ext.mail import Message
from config import BaseConfig

class MailManager():

    def __init__(self, mail):
        self.mail = mail

    def send_email(self, to, subject, template):
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender=BaseConfig.MAIL_DEFAULT_SENDER
        )
        self.mail.send(msg)