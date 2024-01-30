from django import forms
from payapp.models import PayMoney
from payapp.models import Notifications


class PayForm(forms.ModelForm):
    dst_username = forms.CharField(label='Enter the username', required=True)
    class Meta:
        model = PayMoney
        fields = ["dst_username", "transfer_amount"]


class RequestForm(forms.ModelForm):
    other_user = forms.CharField(label='Enter the username', required=True)
    amount = forms.DecimalField(label='Transfer amount', required=True)
    class Meta:
        model = Notifications
        fields = ["other_user", "amount"]
