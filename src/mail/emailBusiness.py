from flask_mail import Message
from flask import current_app, url_for
from handblog import mailed
def to_send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mailed.send(msg)


