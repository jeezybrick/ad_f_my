import re
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div


class MyWidget(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        _widgets = (
            forms.widgets.TextInput(attrs={'size': '4', 'placeholder': '###', 'pattern': '.{3}', 'minlength': '3', 'maxlength': '3'}),
            forms.widgets.TextInput(attrs={'size': '4', 'placeholder': '###', 'pattern': '.{3}', 'minlength': '3', 'maxlength': '3'}),
            forms.widgets.TextInput(attrs={'size': '6', 'placeholder': '####', 'pattern': '.{4}', 'minlength': '4', 'maxlength': '4'}),
        )
        super(MyWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split(' ')
        return [None, None, None]

    def format_output(self, rendered_widgets):
        return (
                   '<div class="row phone-inputs">'
                   '<div class="col-lg-12 col-md-11 col-sm-11 col-xs-12">'
                   '<div class="form-inline">'
                   '<div class="col-md-3 col-xs-3 col-sm-3">%s</div>'
                   '<div class="line-between-phone col-md-1 col-xs-1 col-sm-1 text-center">-<br></div>'
                   '<div class="col-md-3 col-xs-3 col-sm-3">%s</div>'
                   '<div class="line-between-phone col-md-1 col-xs-1 col-sm-1 text-center">-</div>'
                   '<div class="col-md-3 col-xs-3 col-sm-3">%s</div>'
                   '</div>'
                   '</div>'
                   '</div>'
               ) % tuple(rendered_widgets)


class PhoneField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        list_fields = [forms.CharField(),
                       forms.CharField(),
                       forms.CharField()
                       ]
        super(PhoneField, self).__init__(list_fields, widget=MyWidget, *args, **kwargs)

    def compress(self, values):
        return ''.join(values)

    def clean(self, values):
        value = ''.join(values)
        reg = re.compile('\d{10}$')
        if not reg.match(value):
            raise ValidationError(_('Invalid phone format'))


class DemoForm(forms.Form):
    first_name = forms.CharField(label='')
    last_name = forms.CharField(label='')
    email = forms.EmailField(label='', required=True)
    phone = PhoneField(required=True, label='')
    url = forms.URLField(label='', required=False)

    def __init__(self, *args, **kwargs):
        super(DemoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'demo_form'
        self.helper.form_action = '#'
        self.helper.form_class = 'form-horizontal'
        self.helper.field_class = 'col-md-12 '
        self.form_show_errors = True
        self.helper.error_text_inline = True
        self.helper.help_text_inline = False
        self.helper.html5_required = True

        self.helper.add_input(Submit('submit', _('Request demo!'),
                                     css_class='jump-to-form-button'))

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
            Div(
                Field(
                    'phone'
                ), css_class='form-inline'
            )
            ,
            Field(
                'url',
                placeholder=_('Website/URL (optional)')
            )
        )
