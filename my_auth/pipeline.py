from social.pipeline.partial import partial
from django.shortcuts import redirect


@partial
def redirect_to_login_form(backend, user, response, *args, **kwargs):
    # print(kwargs)
    # print(response)
    print(user)
    return redirect('home')
