import requests
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from payapp.models import AccountBal


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label='First Name', required=True)
    last_name = forms.CharField(label='Last Name', required=True)
    CURRENCY = [('GBP',  'GB Pounds'), ('USD', 'US dollars'), ('EUR', 'Euros')]
    currency = forms.CharField(label='Currency', widget=forms.Select(choices=CURRENCY))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", "currency")

    def save(self, commit=True, *args, **kwargs):
        instance = super(RegisterForm, self).save(*args, **kwargs)
        currency = self.cleaned_data['currency']
        if currency != "GBP":
            url = "https://127.0.0.1:8000/conversion/GBP/%s" % currency
            response = requests.get(url, verify="C:/Users/ogarr/Documents/Web Applications and Services/webapps2023/127-0-0-1-chain.pem")
            print(response.json())
            account_bal = 1000*float(response.json()[0]['conversion_rate'])
        else:
            account_bal = 1000
        AccountBal.objects.create(name=instance, account_bal=account_bal, currency=currency)
        return instance
