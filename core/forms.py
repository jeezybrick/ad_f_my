from django import forms
from django.contrib.auth.hashers import make_password
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from django.core.mail import send_mail
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from core.models import Country
from publisher.models import Publisher


class DemoForm(forms.Form):
    first_name = forms.CharField(label='')
    last_name = forms.CharField(label='')
    email = forms.EmailField(label='', required=True)
    phone = forms.CharField(required=True,
                            label='',
                            validators=[validators.RegexValidator(r'^\d{3}\-\d{3}\-\d{4}$',
                                                                  'Invalid phone format!',
                                                                  'invalid'), ])
    company = forms.CharField(required=False, label='')
    url = forms.URLField(label='', required=False)
    website = forms.MultipleChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super(DemoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'demo_form'
        self.helper.form_action = '#'
        self.helper.form_class = 'form-horizontal'
        self.helper.field_class = 'col-lg-4 col-lg-offset-4 col-md-6 col-md-offset-3 ' \
                                  'col-sm-8 col-sm-offset-2 col-xs-10 col-xs-offset-1'
        self.form_show_errors = True
        self.helper.error_text_inline = True
        self.helper.help_text_inline = False
        self.helper.html5_required = True

        self.helper.add_input(Submit('submit', _('Get Early Access'),
                                     css_class='form-button'))

        self.helper.layout = Layout(

            Field(
                'first_name',
                placeholder=_('First name')
            ),
            Field(
                'last_name',
                placeholder=_('Last name')
            )
            ,
            Field(
                'email',
                placeholder=_('Email')
            )

            ,
            Field(
                'phone',
                placeholder=_('###-###-####')
            )
            ,
            Field(
                'company',
                placeholder=_('Company name (optional)')
            )

            ,
            Field(
                'url',
                placeholder=_('http://www.yourwebsite.com (optional)')
            )
        )


class JoinNetworkForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    name = forms.CharField(label='', required=True)
    email = forms.EmailField(label='', required=True,
                             error_messages={'unique': 'Publisher with this Email already exists'})
    telephone = forms.CharField(required=True,
                                label='',
                                validators=[validators.RegexValidator(r'^\d{3}\-\d{3}\-\d{4}$',
                                                                      'Invalid phone format!',
                                                                      'invalid'), ])

    accept = forms.BooleanField(label='', required=True,
                                help_text="<span class=\"accept-joint-network-text\">I accept the "
                                          "<a href=\"/terms/\">Terms & Conditions</a> and "
                                          "<a href=\"/policy/\">Privacy Policy.</a></span>")

    password1 = forms.CharField(label='', min_length=8,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label='', min_length=8,
                                widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(JoinNetworkForm, self).__init__(*args, **kwargs)
        self.fields['country'] = forms.ModelChoiceField(help_text="<hr>",
                                                        queryset=Country.objects.all(),
                                                        label='',
                                                        empty_label='Country')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'join_network_form'
        self.helper.form_action = '#'
        self.helper.form_class = 'form-horizontal'
        self.helper.field_class = 'col-lg-8 col-lg-offset-1 ' \
                                  'col-md-8 col-md-offset-1 ' \
                                  'col-sm-8 col-sm-offset-2 ' \
                                  'col-xs-10 col-xs-offset-1'
        self.form_show_errors = True
        self.helper.error_text_inline = True
        self.helper.help_text_inline = False
        self.helper.html5_required = True

        self.helper.add_input(Submit('submit', _('ACCESS NETWORK'),
                                     css_class='form-button'))

        self.helper.layout = Layout(
            Field(
                'name',
                placeholder=_('Your Name or Publisher Name')
            )
            ,

            Field(
                'telephone',
                placeholder=_('###-###-#### (primary contact number)')
            )
            ,
            Field(
                'country',
                css_class='country_select'
            )
            ,

            Field(
                'email',
                placeholder=_('Email (this will be your login/username)')
            )

            ,
            Field(
                'password1',
                placeholder=_('Password (must be 8 characters)')
            )

            ,
            Field(
                'password2',
                placeholder=_('Confirm Password')
            )

            ,

            Field(
                'accept',
                placeholder=_('')
            )

        )

    class Meta:
        model = Publisher
        fields = ("name", "email", "country", 'telephone',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(JoinNetworkForm, self).save(commit=False)
        user.password = make_password(self.cleaned_data["password1"], salt="adfits")
        user.is_active = False

        if commit:
            user.save()
        return user

    def send_email(self):
        email_to = ['ali@adfits.com', 'info@adfits.com']
        # email_to = ['smooker14@gmail.com']
        email_from = settings.EMAIL_HOST_USER
        subject = 'A NEW PUBLISHER HAS JOINED'

        message = 'Publisher Name: {}\n ' \
                  'Phone:{}\n ' \
                  'Country:{}\n ' \
                  'Email:{}\n\n '.format(
            self.cleaned_data.get('name'),
            self.cleaned_data.get('telephone'),
            self.cleaned_data.get('country'),
            self.cleaned_data.get('email'),
        )

       #  send_mail(subject, message, email_from, email_to, fail_silently=False)


class PublisherProfileForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ("name", "email",)
        widgets = {

        }
