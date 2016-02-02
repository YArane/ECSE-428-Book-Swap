from flask.ext.mail import Message
from BookSwap import app, mail

def send_email(to, subject, template):
	msg = Messasge(
		subject,
		recipients=[to],
		html=template,
		sender=app.config['MAIL_DEFAULT_SENDER']
		)
	mail.send(msg)