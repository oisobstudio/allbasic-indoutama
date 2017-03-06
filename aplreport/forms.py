from django import forms



class FormReportSaleWebsite(forms.Form):
	from_date = forms.CharField()
	to_date = forms.CharField()


class FormReportAllSalePerdate(forms.Form):
	from_date = forms.CharField()
	to_date = forms.CharField()


class FormReportingSaleStore(forms.Form):
	from_date = forms.CharField()
	to_date = forms.CharField()


class FormReportingSaleWeb(forms.Form):
	from_date = forms.CharField()
	to_date = forms.CharField()


class FormReportingSaleArticle(forms.Form):
	from_date = forms.CharField()
	to_date = forms.CharField()
