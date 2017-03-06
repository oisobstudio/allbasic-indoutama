from django import forms


class FormAccountLogin(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)


