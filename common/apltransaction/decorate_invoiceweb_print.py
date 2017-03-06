from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect
from django.core.urlresolvers import reverse
from apltransaction.models import TransactionDetail, Invoice
from django.shortcuts import get_object_or_404
from django.contrib import messages


def validate_print(f):
	def wrap(request, *args, **kwargs):
		invoice_number = kwargs.get('invoice_number')

		if invoice_number:
			invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
			if invoice.transactiondetail_set.count() == 0:
				msg = "Item is empty !"
				messages.warning(request, msg)
				data_kwargs = {'invoice_number': invoice_number}
				return HttpResponseRedirect(reverse('apltransaction:transactiondetailweb_add', kwargs=data_kwargs))

		return f(request, *args, **kwargs)

	wrap.__doc__ = f.__doc__
	wrap.__name__ = f.__name__
	return wrap