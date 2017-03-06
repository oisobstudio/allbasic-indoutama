from django import forms
from .models import Invoice, TransactionDetail


class FormAddTransactionDetail(forms.ModelForm):
    class Meta:
        model = TransactionDetail
        fields = ('article_code', 'article_name', 'article_size',
                  'article_price', 'quantity', 'sub_total')


class FormAddTransactionStoreDetail(forms.ModelForm):
	class Meta:
		model = TransactionDetail
		fields = ('article_code',)


class FormAddTransactionWebDetail(forms.ModelForm):
    class Meta:
        model = TransactionDetail
        fields = ('article_code', 'article_name', 'article_size',
                  'article_price', 'quantity', 'sub_total')


class FormSearchInvoice(forms.Form):
    query = forms.CharField()


class FormInvoiceWebChangeStatus(forms.ModelForm):
  class Meta:
    model = Invoice
    fields = ('status',)
