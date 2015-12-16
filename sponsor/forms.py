from django import forms
from sponsor.models import Sponsor, Industry

class SponsorForm(forms.ModelForm):
    """
    This form will used while adding/editting publisher.
    """
    
    class Meta:
        model = Sponsor

    def __init__(self, *args, **kwargs):
        super(SponsorForm, self).__init__(*args, **kwargs)
        self.fields['industry'] = forms.ModelChoiceField(
        	Industry.objects.all(), required=False
        )
