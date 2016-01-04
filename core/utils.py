import datetime
from django.core.mail import send_mail
from django.conf import settings


def send_email_with_form_data(data):
    email_to = ['ali@adfits.com', 'info@adfits.com']
    # email_to = ['arsenij.sychev@gmail.com']
    email_from = settings.EMAIL_HOST_USER
    subject = 'REQUEST FOR ACCESS'

    message = 'First Name: {}\n ' \
              'Last Name:{}\n ' \
              'Email:{}\n ' \
              'Phone:{}\n ' \
              'Company (optional):{}\n ' \
              'Website (optional):{}\n\n ' \
              'Date of request:{}'.format(
        data.get('first_name', default=None),
        data.get('last_name', default=None),
        data.get('email', default=None),
        data.get('phone', default=None),
        check_is_empty(data.get('company', default='---')),
        check_is_empty(data.get('url', default='---')),
        datetime.datetime.now().date().strftime('%m/%d/%Y')
    )

    send_mail(subject, message, email_from, email_to, fail_silently=False)


def send_email_with_form_data_join(data):
    email_to = ['ali@adfits.com', 'info@adfits.com']
    email_from = settings.EMAIL_HOST_USER
    subject = 'A NEW PUBLISHER HAS JOINED'

    message = 'Publisher Name: {}\n ' \
              'Phone:{}\n ' \
              'Country:{}\n ' \
              'Email:{}\n\n '.format(
        data.get('name', default=None),
        data.get('telephone', default=None),
        data.get('country', default=None),
        data.get('email', default=None),
    )

    # send_mail(subject, message, email_from, email_to, fail_silently=False)


def check_is_empty(value):
    if not value:
        return '----'
    return value

