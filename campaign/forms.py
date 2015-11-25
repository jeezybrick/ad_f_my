from django import forms
from django.contrib.admin import widgets   
from campaign.models import Campaign, Widget
from publisher.models import Publisher, Website
from sponsor.models import Sponsor, Industry

class CampaignForm(forms.ModelForm):
    """
    This form will used while adding/editting campaigns.
    """

    class Meta:
        model = Campaign
        exclude = ('sponsor',)
        
    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)
        self.fields['website'] = forms.ModelChoiceField(Website.objects.all())
        

class WidgetForm(forms.ModelForm):
    """
    This form will used while adding/editting campaigns.
    """

    class Meta:
        model = Widget

    def __init__(self, *args, **kwargs):
        super(WidgetForm, self).__init__(*args, **kwargs)
        self.fields['campaign'] = forms.ModelChoiceField(
            Campaign.objects.all()
        )

class SponsorCampaignForm(CampaignForm):
    """
    """

    def __init__(self, *args, **kwargs):
        super(SponsorCampaignForm, self).__init__(*args, **kwargs)
        self.fields['campaign_name'].widget = forms.TextInput(attrs={
            'type':'text', 'placeholder':'Enter Campaign name',
            'class': 'form-control', 'style': 'height: 25px'
        })
 
        self.fields['end_date'].widget = forms.TextInput(attrs={
            'autocomplete' : 'off',
            'class' : 'input-large',
            'data-datepicker' : 'datepicker'
        })

        self.fields['start_date'].widget = forms.TextInput(attrs={
            'autocomplete' : 'off',
            'class' : 'input-large',
            'data-datepicker' : 'datepicker'
        })
