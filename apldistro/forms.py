# Django package import
from django import forms
# This app import
from .models import Store
from .models import Brand
from .models import Profile


class StoreFormAdd(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['owner', 'name', 'founding_date', 'about', 'logo', 'address']


class FormStoreAdd(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['owner', 'name', 'founding_date', 'about', 'logo', 'address']
            

class FormStoreChange(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'founding_date', 'about', 'logo', 'address']


class FormBrandAdd(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'about', 'logo']


class FormBrandChange(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'about', 'logo']

