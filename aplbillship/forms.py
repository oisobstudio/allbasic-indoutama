from django import forms
from .models import Billing, Shipping


class FormAddBilling(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ('name', 'email', 'phone')


class FormAddShipping(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ('province', 'city', 'vendor', 'pack', 'address', 'price')
