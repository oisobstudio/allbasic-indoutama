from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Sum
from apltransaction.models import Invoice
from aplhelper.helpers import helper_generate_code
from .models import Billing, Shipping
from .forms import FormAddBilling
from .forms import FormAddShipping

# ===================
# dataresource module
# ===================
from dataresource.models import HoldTarget


def billing_add(request, invoice_number):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
    if request.method == 'POST':
        form = FormAddBilling(request.POST)
        if form.is_valid():
            billing = form.save(commit=False)
            billing.code = helper_generate_code()
            billing.invoice = invoice
            billing.save()

            # Hold Target
            # -----------
            try:
                hold_target = HoldTarget.objects.get(invoice_number=invoice.invoice_number)
                current_state = hold_target.state
                hold_target.state = current_state + 1
                hold_target.save()
            except:
                pass

            data_context_kwargs = {'invoice_number': invoice_number}
            return HttpResponseRedirect(reverse('apltransaction:transactiondetailweb_add', kwargs=data_context_kwargs))
    else:
        form = FormAddBilling()

    data_context = {'invoice': invoice, 'form': form}
    return render(request, 'aplbillship/billing/billing_add.html', data_context)


def billing_remove(request, invoice_number, code):
    # ambil data invoice
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
    # ambil data billing
    billing = get_object_or_404(Billing, code=code, invoice=invoice)
    # hapus data billing
    billing.delete()
    # kembali ke halaman tambah billing
    data_kwargs = {'invoice_number': invoice_number}
    return HttpResponseRedirect(reverse('apltransaction:transactiondetailweb_add', kwargs=data_kwargs))


def shipping_add(request, invoice_number):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
    if request.method == 'POST':
        form = FormAddShipping(request.POST)
        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.code = helper_generate_code()
            shipping.invoice = invoice
            shipping.save()
            data_context_kwargs = {'invoice_number': invoice_number}
            # Hold Target
            # -----------
            try:
                hold_target = HoldTarget.objects.get(invoice_number=invoice.invoice_number)
                current_state = hold_target.state
                hold_target.state = current_state + 1
                hold_target.save()
            except:
                pass

            return HttpResponseRedirect(reverse('apltransaction:transactiondetailweb_add', kwargs=data_context_kwargs))
    else:
        form = FormAddShipping()

    data_context = {'form': form, 'invoice': invoice}
    return render(request, 'aplbillship/shipping/shipping_add.html', data_context)


def shipping_remove(request, invoice_number, code):
    # mengambil invoice
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
    # mengambil shipping
    shipping = get_object_or_404(Shipping, invoice=invoice, code=code)
    # menghapus data shipping
    shipping.delete()
    # redirect ke halaman form tambah shipping (shipping_add)
    data_kwargs = {'invoice_number': invoice_number}
    return HttpResponseRedirect(reverse('apltransaction:transactiondetailweb_add', kwargs=data_kwargs))


