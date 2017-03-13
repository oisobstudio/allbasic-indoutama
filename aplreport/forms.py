from django import forms
from apldistro.models import Brand


class FormReportSalesGrow(forms.Form):
	from_date = forms.CharField()
	to_date = forms.CharField()


class FormReportSalesNet(forms.Form):
	from_date = forms.CharField()
	to_date = forms.CharField()


class FormReportInvoice(forms.Form):
	from_date = forms.CharField()
	to_date = forms.CharField()

