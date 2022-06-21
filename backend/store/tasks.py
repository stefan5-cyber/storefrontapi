from celery import shared_task
from django.core.mail import EmailMessage, BadHeaderError


@shared_task
def notify_customer(order):
    print(order)
    try:
        message = EmailMessage(
            'subject', str(order), 'stefan5@lwa.com', ['john@doe.com']
        )
        message.send()
    except BadHeaderError:
        pass
