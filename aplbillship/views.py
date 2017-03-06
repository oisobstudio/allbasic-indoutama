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



def billing_add(request, invoice_number):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
    if request.method == 'POST':
        form = FormAddBilling(request.POST)
        if form.is_valid():
            billing = form.save(commit=False)
            billing.code = helper_generate_code()
            billing.invoice = invoice
            billing.save()
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
            return HttpResponseRedirect(reverse('apltransaction:transactiondetailweb_add', kwargs=data_context_kwargs))
    else:
        form = FormAddShipping()

    data_context = {'form': form, 'invoice': invoice, 'state_rajaongkir': settings.RAJAONGKIR_STATE}
    return render(request, 'aplbillship/shipping/shipping_add.html', data_context)


def shipping_add_manual(request, invoice_number):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
    if request.method == 'POST':
        form = FormAddShipping(request.POST)
        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.code = helper_generate_code()
            shipping.invoice = invoice
            shipping.save()
            data_context_kwargs = {'invoice_number': invoice_number}
            return HttpResponseRedirect(reverse('apltransaction:transactiondetailweb_add', kwargs=data_context_kwargs))
    else:
        form = FormAddShipping()

    data_context = {'form': form, 'invoice': invoice}
    return render(request, 'aplbillship/shipping/shipping_add_manual.html', data_context)

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


def ajax_getallprovince(request):

    if request.is_ajax():
        import http.client
        import json
        conn = http.client.HTTPConnection(settings.RAJAONGKIR_URL)
        headers = {'key': settings.RAJAONGKIR_KEYAPI}
        conn.request("GET", "/starter/province", headers=headers)
        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        data = json.loads(data)
        data = data['rajaongkir']['results']
        data = json.dumps(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def ajax_getallcity(request, province_id):
    if request.is_ajax():
        import http.client
        import json
        conn = http.client.HTTPConnection(settings.RAJAONGKIR_URL)
        headers = {'key': settings.RAJAONGKIR_KEYAPI}
        conn.request("GET", "/starter/city?province={}".format(province_id), headers=headers)
        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        data = json.loads(data)
        data = data['rajaongkir']['results']
        data = json.dumps(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def ajax_getpackage(request, invoice_number, city_id, vendor):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
    # ambil jumlah keseluruhan barang dari item transaction detail berdasarkan invoicenya
    totalquantity = invoice.transactiondetail_set.all().aggregate(tquantity=Sum('quantity'))
    

    if request.is_ajax():
        import http.client
        import json
        conn = http.client.HTTPConnection(settings.RAJAONGKIR_URL)
        weight = 400 * totalquantity['tquantity']
        payload = "origin={city_state}&destination={city_destination}&weight={weight}&courier={vendor}"
        payload = payload.format(city_state=str(settings.RAJAONGKIR_STATE['id']), # kota kantor
                                 city_destination=str(city_id),  # kota yang mau dikirim
                                 vendor=vendor, # vendor JNE
                                 weight=weight)  
        headers = {
            'key': settings.RAJAONGKIR_KEYAPI,
            'content-type': "application/x-www-form-urlencoded"
        }

        conn.request("POST", "/starter/cost", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        data = json.loads(data)
        data = data['rajaongkir']['results'][0]['costs']
        data = json.dumps(data)

    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)