from django import forms
from .models import Discount


class FormDiscountAdd(forms.ModelForm):
	class Meta:
		model = Discount
		fields = '__all__'
		exclude = ['code',]

		
class FormDiscountChange(forms.ModelForm):
	class Meta:
		model = Discount
		fields = '__all__'
		exclude = ['code',]

