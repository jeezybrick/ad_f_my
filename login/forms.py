from django import forms
from django.utils.translation import ugettext_lazy as _
from backend import authenticate
from my_auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    email = forms.EmailField(required=True,
        widget=forms.TextInput(attrs={
            'type': 'email', 'placeholder': 'Enter your email', 'class': 'span'
        }))
    password = forms.CharField(
        max_length=20, widget=forms.TextInput(attrs={
            'type': 'password', 'placeholder': 'Password', 'class': 'span'
        }))


class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'type': 'password', 'placeholder': 'Your Old Password', 'class': 'span'
    }))
    new_password = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'type': 'password', 'placeholder': 'New Password', 'class': 'span'
    }))
    confirm_password = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'type': 'password', 'placeholder': 'Confirm Password', 'class': 'span'
    }))

    def __init__(self, model=None, username=None, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.username = username or ''
        self.model = model or ''

    def clean_old_password(self):
        password = self.cleaned_data['old_password']
        user = authenticate(self.model, username=self.username, password=password)

        if user is None:
            raise forms.ValidationError(_("Old password does match for the user."))
        return self.cleaned_data

    def clean_confirm_password(self):
        if self.cleaned_data['new_password'] != self.cleaned_data['confirm_password']:
            raise forms.ValidationError(
                _("New Password and Confirm Password did not match.")
            )
        return self.cleaned_data
