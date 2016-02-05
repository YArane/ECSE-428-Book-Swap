from flask.ext.mail import Message
from config import BaseConfig

class MailManager():

    def __init__(self, mail, app):
        self.mail = mail
        self.app = app

    def send_email(self, to, subject, template):
        print "sending mail!"
        print "destination: " + to
        print "templates: " + template
        print "send: " + BaseConfig.MAIL_USERNAME
        print "subject: " + subject
        msg = Message(
            subject,
            recipients=[to],
            body=template,
            sender=BaseConfig.MAIL_USERNAME
        )

        with self.app.app_context():
            self.mail.send(msg)