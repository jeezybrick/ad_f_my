import datetime
from django.core.mail import send_mail


def send_email_with_form_data(data):
    email_to = ['ali@adfits.com', 'info@adfits.com']
    email_from = ''
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
        data.get('company', default='---'),
        data.get('url', default='---'),
        datetime.datetime.now().date().strftime('%m/%d/%Y')
    )

    send_mail(subject, message, email_from, email_to, fail_silently=False)
