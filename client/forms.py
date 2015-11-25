import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

        
class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'type':'text', 'placeholder':'Enter your email','class': 'span'
    }))
    password = forms.CharField(
        max_length = 20, widget=forms.TextInput(attrs={
            'type':'password', 'placeholder':'Password',  'class': 'span'
    }))


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
    	'type':'text', 'placeholder':'Your E-mail',  'class': 'span'
    }))

    class Meta:
        model = User
        fields = ('username', 'email',) 

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'type':'text', 'placeholder':'Enter your name', 'class': 'span'
        })
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'type':'password', 'placeholder':'Confirm Password', 'class': 'span'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'type':'password', 'placeholder':'Confirm Password', 'class': 'span'
        })

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("This email address already exists.")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.is_active = True # change to false if using email activation
        if commit:
            user.save()
            
        return user

from django.contrib.auth import authenticate
class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={
        'type':'password', 'placeholder':'your old Password',  'class' : 'span'
    }))
    new_password = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={
        'type':'password', 'placeholder':'New Password',  'class' : 'span'
    }))
    confirm_password = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={
        'type':'password', 'placeholder':'Confirm Password',  'class' : 'span'
    }))

    def __init__(self, request=None, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.email = ''

        if request is not None:
            self.email = request.user.email
       
    def clean_old_password(self):
        password = self.cleaned_data['old_password']
        user = authenticate(username=self.email, password=password)

        if user is None:
            raise forms.ValidationError(_("Old password does match for the user."))  
        return self.cleaned_data

    def clean_confirm_password(self):
        if self.cleaned_data['new_password'] != self.cleaned_data['confirm_password']:
            raise forms.ValidationError(
                _("New Password and Confirm Password did not match.")
            )
        return self.cleaned_data