from django import forms
from account.models import Account
from django_countries.fields import CountryField


class AccountAdminForm(forms.ModelForm):
    location = forms.ChoiceField(choices=CountryField().choices)

    class Meta:
        model = Account
        fields = '__all__'
