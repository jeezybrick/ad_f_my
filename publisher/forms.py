from django import forms
from publisher.models import Publisher, Website
from sponsor.models import Industry
from login.backend import authenticate


class PublisherForm(forms.ModelForm):
    """
    This form will used while adding/editting publisher.
    """

    class Meta:
        model = Publisher

    def __init__(self, *args, **kwargs):
        super(PublisherForm, self).__init__(*args, **kwargs)
        self.fields['industry'] = forms.ModelChoiceField(Industry.objects.all(), required=False)


class WebsiteForm(forms.ModelForm):
    """
    This form will used while adding/editting websites.
    """

    class Meta:
        model = Website

    def __init__(self, *args, **kwargs):
        super(WebsiteForm, self).__init__(*args, **kwargs)
        self.fields['industry'] = forms.ModelChoiceField(Industry.objects.all(), required=False)


class WebsiteNewForm(forms.ModelForm):
    """
    This form will used while adding/editting websites.
    """

    class Meta:
        model = Website
        fields = ("website_name", "website_domain", )


class PublisherWebsiteForm(WebsiteForm):
    """
    Custom form to be used for add/edit websites
    """

    def __init__(self, *args, **kwargs):
        super(PublisherWebsiteForm, self).__init__(*args, **kwargs)
        self.fields['website_name'].widget = forms.TextInput(
            attrs={'type': 'text', 'placeholder': 'Enter website name', 'class': 'form-control input-small',
                'style': 'height: 25px'})
        self.fields['website_domain'].widget = forms.TextInput(
            attrs={'type': 'url', 'placeholder': 'Enter your website domain', 'class': 'form-control input-small',
                'style': 'height: 25px'})
        self.fields['twitter_name'].widget = forms.TextInput(
            attrs={'type': 'text', 'placeholder': '@', 'class': 'form-control input-small', 'style': 'height: 25px'})
        self.fields['facebook_page'].widget = forms.TextInput(
            attrs={'type': 'url', 'placeholder': 'http://', 'class': 'form-control input-small',
                'style': 'height: 25px'})
        self.fields['avg_page_views'].widget = forms.TextInput(
            attrs={'type': 'number', 'placeholder': 'There are no minimums, so please be honest!',
                'class': 'form-control input-small', 'style': 'height: 25px'})


class AddwebsiteForm(forms.ModelForm):
    """
    This form will used while adding/editting websites in the front end.
    """
    name = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': 'Enter website name', 'class': 'span input-xlarge',
            "style": "height:15px", 'required': "", }))
    domain = forms.URLField(initial='http://', widget=forms.TextInput(
        attrs={'type': 'url', 'placeholder': 'Enter your website domain', 'class': 'span input-xlarge',
            "style": "height:15px", 'required': "", }))
    industry = forms.ModelChoiceField(queryset=Industry.objects.all())
    logo = forms.FileField()

    class Meta:
        model = Website


class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'type': 'password', 'placeholder': 'your old Password', 'class': 'span'}))
    new_password = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'type': 'password', 'placeholder': 'New Password', 'class': 'span'}))
    confirm_password = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'type': 'password', 'placeholder': 'Confirm Password', 'class': 'span'}))

    def __init__(self, request=None, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.username = ''

        if request is not None:
            username = request.session['_id']

    def clean_old_password(self):
        password = self.cleaned_data['old_password']
        user = authenticate("Publisher", username=self.username, password=password)

        if user is None:
            raise forms.ValidationError(_("Old password does match for the user."))
        return self.cleaned_data

    def clean_confirm_password(self):
        if self.cleaned_data['new_password'] != self.cleaned_data['confirm_password']:
            raise forms.ValidationError(_("New Password and Confirm Password did not match."))
        return self.cleaned_data
