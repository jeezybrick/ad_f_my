from django.core.mail import send_mail


def send_email_with_form_data(data):

    email_from = 'smooker14@gmail.com'
    email_to = 'smooker14@gmail.com'
    subject = 'demo_subject'
    phone = data.get('phone_0', default=None) + '-' + \
            data.get('phone_1', default=None)+'-' + \
            data.get('phone_2', default=None)

    message = ' First name: {}\n Last name:{}\n Email:{}\n Phone:{}\n Web:{}\n'.format(
        data.get('first_name', default=None),
        data.get('last_name', default=None),
        data.get('email', default=None),
        phone,
        data.get('url', default='---'),
    )

    send_mail(subject, message, email_from, [email_to], fail_silently=False)
