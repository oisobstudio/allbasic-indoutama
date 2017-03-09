from django import forms
from apldistro.models import Brand



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


class FormLaporanArtikelDiminati(forms.Form):
	from_date = forms.CharField()
	to_date = forms.CharField()


class FormLaporanTrafikBrand(forms.Form):
	brand = forms.ModelMultipleChoiceField(queryset=Brand.objects.all() )
	from_date = forms.CharField()
	to_date = forms.CharField()