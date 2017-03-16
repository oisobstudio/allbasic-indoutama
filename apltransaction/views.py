# ======================
# Built-in Python module
# ======================
from datetime import date
import json

# ==================
# Django part module
# ==================
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError, transaction as trans
from django.contrib import messages
from django.db.models import Sum, PositiveIntegerField, Q, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction as trans
from django.views.generic import View

# ================
# Inner app module
# ================
from .models import Invoice
from .models import TransactionDetail 
from .models import InvoiceCategory
from .models import InvoiceStatus
from .forms import FormAddTransactionDetail
from .forms import FormAddTransactionStoreDetail
from .forms import FormSearchInvoice
from .forms import FormAddTransactionWebDetail
from .forms import FormInvoiceWebChangeStatus

# ====================
# aplhelper app module
# ====================
from aplhelper.helpers import helper_generate_code, helper_session_brand_pk
from common.decorators import connecting_brand_required
from aplpromotion.models import Discount

# =======================
# aplinventory app module
# =======================
# from aplinventory.models import BrandArticleDetail, Article
from aplinventory.views import helper_generate_code
from aplinventory.models import ArticleDetail, Article

from apldistro.models import Profile, Store, Brand
from aplbillship.models import Billing, Shipping
from apltransaction.models import InvoiceStatus

# ===================
# dataresource module
# ===================
from dataresource.models import HoldTarget



## =============================================================================
##                                  INVOICE (GENERAL)
## =============================================================================

def ajax_invoice_remove_hold_and_invalid(request):
    if request.is_ajax():
        total_invoices_invalid = 0
        total_article_back = 0
        total_invoices_cancel = 0

        if request.method == 'POST':
            try:
                # mendapatkan data dari ajax post dan merubah ke json string format utf-8
                json_string = request.body.decode(encoding='UTF-8')
                # merubah string json ke dictionary python
                dict_data = json.loads(json_string)

                # ambil semua data invoice yang tidak ada item transactiondetail-nya.
                invoices_invalid = Invoice.objects.filter(transactiondetail=None)
                print(invoices_invalid)
                total_invoices_invalid = invoices_invalid.count()
                if invoices_invalid.count() > 0:
                    invoices_invalid.delete()
            except:
                pass

            try:
                # ambil semua data invoice yang tidak ada shipping yang berlaku untuk web
                invoices_nobill = Invoice.objects.filter(billing=None, category__abbv='W')
                # hapus data
                for inv in invoices_nobill:
                    if inv.transactiondetail_set.count() == 0:
                        inv.delete()
                    elif inv.transactiondetail_set.count() > 0:
                        # mengupdate stock article detail dari quantity pda transaction detail
                        for td in inv.transactiondetail_set.all():
                            articledetail = ArticleDetail.objects.get(
                                code=td.article_code)
                            stock = articledetail.stock
                            articledetail.stock = stock + td.quantity
                            articledetail.save()
                            total_article_back += 1

                        inv.delete()
            except:
                pass

            try:
                # ambil semua data invoice yang tidak ada billing yang berlaku untuk web
                invoices_noshipp = Invoice.objects.filter(shipping=None, category__abbv='W')
                # hapus data
                for inv in invoices_noshipp:
                    if inv.transactiondetail_set.count() == 0:
                        inv.delete()
                    elif inv.transactiondetail_set.count() > 0:
                        # mengupdate stock article detail dari quantity pda transaction detail
                        for td in inv.transactiondetail_set.all():
                            articledetail = ArticleDetail.objects.get(
                                code=td.article_code)
                            stock = articledetail.stock
                            articledetail.stock = stock + td.quantity
                            articledetail.save()
                            total_article_back += 1

                        inv.delete()
            except:
                pass

            try:
                # ambil semua data invoice yang statusnya hold
                invoices_hold = Invoice.objects.filter(status__abbv='H', category__abbv='W')
                # hapus data
                for inv in invoices_hold:
                    if inv.transactiondetail_set.count() == 0:
                        inv.delete()
                    elif inv.transactiondetail_set.count() > 0:
                        # mengupdate stock article detail dari quantity pda transaction detail
                        for td in inv.transactiondetail_set.all():
                            articledetail = ArticleDetail.objects.get(
                                code=td.article_code)
                            stock = articledetail.stock
                            articledetail.stock = stock + td.quantity
                            articledetail.save()
                            total_article_back += 1

                        status = InvoiceStatus.objects.filter(abbv='C')
                        if status.exists():
                            inv.status = status[0]
                            total_invoices_cancel += 1
                            print("nah kan")
                            inv.save()
                        else:
                            inv.delete()
            except:
                pass

            
            dict_data = {
                'total_invoices_invalid': total_invoices_invalid,
                'total_article_back': total_article_back,
                'total_invoices_cancel': total_invoices_cancel
            }
            
            return HttpResponse(json.dumps(dict_data), content_type='application/json')

        else:
            return HttpResponse(json.dumps({'status': False}), content_type='application/json')
    else:
        return render(request, 'apltransaction/invoice/ajax_invoice_remove_hold_and_invalid.html', {})




## =============================================================================
##                                  INVOICE STORE                                       
## =============================================================================


def invoicestore_list(request):
    invoices = Invoice.objects.filter(category__abbv='S').exclude(Q(transactiondetail=None)).order_by('-invoice_date')
    # invoices = Invoice.objects.filter(category__abbv='S').exclude(Q(transactiondetail=None)).order_by('-invoice_date')
    form = FormSearchInvoice()

    # =================================
    # Pencarian invoice dari input text 
    # =================================
    if 'query' in request.GET:
        form = FormSearchInvoice(request.GET)

        if form.is_valid():
            cd = form.cleaned_data
            invoices = invoices.filter(
                Q(invoice_number__icontains=cd['query']) | 
                Q(user__username__icontains=cd['query']) | 
                Q(transactiondetail__article_name__icontains=cd['query']) | 
                Q(category__abbv__icontains=cd['query'][0])).distinct()

    # =================================================
    # Filter invoice dari tombol filter (Version 1.0.0)
    # =================================================
    if 'status' in request.GET:
        data_status = request.GET.get('status')
        invoicestatus = get_object_or_404(InvoiceStatus, abbv=data_status)
        invoices = invoices.filter(status=invoicestatus)

    # ================================
    # Paginasi halaman (Version 1.0.0)
    # ================================
    paginator = Paginator(invoices, 7)
    page = request.GET.get('page')
    try:
        invoices = paginator.page(page)
    except PageNotAnInteger:
        invoices = paginator.page(1)
    except EmptyPage:
        invoices = paginator.page(paginator.num_pages)

    data_context = {'invoices': invoices, 'form': form, 'total_count': invoices}
    return render(request, 'apltransaction/invoice/invoicestore_list.html', 
        data_context)


def invoicestore_add(request):
    invoicecategory = get_object_or_404(InvoiceCategory, abbv='S')

    invoicestatus = get_object_or_404(InvoiceStatus, abbv='F')

    invoice = Invoice(user=request.user, invoice_number=helper_generate_code(),
        total=0, category=invoicecategory, status=invoicestatus)
    invoice.save()

    return HttpResponseRedirect(
        reverse('apltransaction:transactiondetailstore_add', 
            kwargs={'invoice_number': invoice.invoice_number}))


def invoicestore_remove(request, invoice_number):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)

    if invoice.transactiondetail_set.count() > 0:
        for item in invoice.transactiondetail_set.all():
            try:
                article = ArticleDetail.objects.get(code=item.article_code)
                stock_article = article.stock
                article.stock = stock_article + item.quantity
                article.save()
            except:
                pass

    invoice.delete()
    return HttpResponseRedirect(reverse('apltransaction:invoicestore_list'))


def invoicestore_print(request, invoice_number):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)

    store = Store.objects.first()

    transactiondetails = invoice.transactiondetail_set.all()

    data_context = {'invoice': invoice, 
    'transactiondetails': transactiondetails, 'store': store}
    return render(request, 'apltransaction/invoice/invoicestore_print.html', 
        data_context)


def transactiondetailstore_add(request, invoice_number):
    """ Menambahkan TransactionDetail untuk invoice toko.
    =====================================================
    """
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
    transactiondetails = TransactionDetail.objects.filter(invoice=invoice)
    quantity = 1

    if request.method == 'POST':
        form = FormAddTransactionStoreDetail(data=request.POST)

        if form.is_valid():
            transactiondetail = form.save(commit=False)

            # =========================
            # Pemeriksaan ArticleDetail
            # =========================
            articledetails = ArticleDetail.objects.filter(code=transactiondetail.article_code)

            if articledetails:
                articledetail = ArticleDetail.objects.get(code=transactiondetail.article_code)
            else:                
                messages.warning(request, 'The article you are looking for can not be found !')
                return HttpResponseRedirect(reverse('apltransaction:transactiondetailstore_add', 
                    kwargs={'invoice_number': invoice_number}))

            # ======================================
            # Pemeriksaan stock untuk article detail
            # ======================================
            if articledetail.stock - quantity < 0 or quantity <= 0:
                messages.warning(request, 'Stock ordered a very limited number of stocks entirely')

            else:
                # ==========================================================
                # Pengecekan TransactionDetail yang belum ada atau sudah ada
                # ==========================================================
                transdet = TransactionDetail.objects.filter(
                    user=request.user, 
                    invoice=invoice, 
                    article_size=articledetail.size.name,
                    article_code=articledetail.code, 
                    article_name=articledetail.article.name
                )

                if transdet:
                    # ================================
                    # TransactionDetail yang sudah ada
                    # ================================
                    transdet = TransactionDetail.objects.get(user=request.user, 
                        invoice=invoice, article_size=articledetail.size.name,
                        article_code=articledetail.code, 
                        article_name=articledetail.article.name
                    )
                    current_quantity = transdet.quantity
                    new_quantity = quantity + current_quantity
                    transdet.quantity = new_quantity
                    transdet.sub_total = transdet.article_price * new_quantity
                    transdet.save()
                    invoice_total = invoice.transactiondetail_set.aggregate(
                        pricing=Sum('sub_total'))
                    invoice.total = invoice_total.get("pricing")
                    invoice.save()
                    articledetail.stock = articledetail.stock - quantity
                    articledetail.save()

                else:
                    # ================================
                    # TransactionDetail yang belum ada
                    # ================================
                    transdet = TransactionDetail.objects.create(
                        user=request.user, 
                        invoice=invoice, 
                        article_brand_code=articledetail.brand.code,
                        article_brand_name=articledetail.brand.name,
                        article_size=articledetail.size.name,
                        article_code=articledetail.code, 
                        article_name=articledetail.article.name,
                        article_price=articledetail.article.price,
                        article_capitalprice=articledetail.article.capital_price,
                        quantity=quantity,
                        sub_total=(articledetail.article.price * quantity),
                    )

                    invoice_total = invoice.transactiondetail_set.aggregate(
                        pricing=Sum('sub_total'))
                    invoice.total = invoice_total.get("pricing")
                    invoice.save()

                    articledetail.stock = articledetail.stock - quantity
                    articledetail.save()

                # ===================
                # Pengecekan Discount
                # ===================
                
                import datetime

                current_date = datetime.datetime.now()
                invoice_category = invoice.category
                article = articledetail.article

                try:
                    discount = Discount.objects.get(place=invoice_category, article=article)
                except:
                    discount = None

                if discount:
                    # ============================================================
                    # Pemotongan harga pada TransactionDetail berdasarkan Discount
                    # ============================================================
                    

                    discount = discount
                    cut = transdet
                    transdet.sub_total = transdet.sub_total - (transdet.quantity * discount.cut_price)
                    transdet.discount_code = discount.code
                    transdet.discount_name = discount.name
                    transdet.cut_price = discount.cut_price
                    transdet.save()

                    invoice_total = invoice.transactiondetail_set.aggregate(pricing=Sum('sub_total'))
                    invoice.total = invoice_total.get("pricing")
                    invoice.save()

            return HttpResponseRedirect(reverse('apltransaction:transactiondetailstore_add',
                                                kwargs={'invoice_number': invoice_number}))
    else:
        form = FormAddTransactionStoreDetail()

    data_context = {'invoice': invoice, 'transactiondetails': transactiondetails, 'form': form}
    return render(request, 'apltransaction/transactiondetail/transactiondetailstore_add.html', data_context)


def transactiondetailstore_remove(request, invoice_number, article_code):
    """
    fungsi yang digunakan untuk menghapus item pada invoice store.
    fungsi ini ada karena jika seorang admin ingin memiliki item
    pada invoice namun jumlah quantity itemnya ingin diganti atau
    item yang dipesan salah.

    setiap item yang dihapus, quantity akan dikembalikan ke stok
    pada detail artikel.
    """

    # ambil invoice
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
    # ambil transaction detail (item)
    transactiondetail = get_object_or_404(TransactionDetail, article_code=article_code, invoice=invoice)
    # ambil detail article dari code. karena code transaction detail sama dengan
    # code milik article detail 
    articledetail = get_object_or_404(ArticleDetail, code=article_code)
    # ambil quantity
    quantity = transactiondetail.quantity
    # ambil jumlah stock saat ini
    current_stock = articledetail.stock
    # ambil total harga pada invoice
    total = invoice.total
    # set stock invoice yang baru
    articledetail.stock = quantity + current_stock
    # ubah harga pada invoice
    invoice.total = total - transactiondetail.sub_total
    # simpan article detail
    articledetail.save()
    # simpan invoice
    invoice.save()
    # hapus item
    transactiondetail.delete()

    # kembali ke halaman transaction detail web
    data_kwargs = {'invoice_number': invoice.invoice_number}

    return HttpResponseRedirect(reverse('apltransaction:transactiondetailstore_add',
                                        kwargs=data_kwargs))


## ======================================================================================
##                                  INVOICE WEB
## ======================================================================================

@connecting_brand_required
def invoiceweb_list(request):
    brand = helper_session_brand_pk(request)
    if request.user.is_superuser:
        invoices = Invoice.objects.exclude(Q(transactiondetail=None)|Q(shipping=None)|Q(billing=None)).order_by('-invoice_date')
    else:
        invoices = Invoice.objects.distinct().filter(transactiondetail__article_brand_name=brand.name).exclude(Q(transactiondetail=None)|Q(shipping=None)|Q(billing=None)).order_by('-invoice_date')
    form = FormSearchInvoice()

    # =================================
    # Pencarian invoice dari input text 
    # =================================
    if 'query' in request.GET:
        form = FormSearchInvoice(request.GET)

        if form.is_valid():
            cd = form.cleaned_data
            invoices = invoices.filter(
                Q(invoice_number__icontains=cd['query']) | 
                Q(user__username__icontains=cd['query']) | 
                Q(transactiondetail__article_name__icontains=cd['query']) | 
                Q(category__abbv__icontains=cd['query'][0])).distinct()

    # =================================================
    # Filter invoice dari tombol filter (Version 1.0.0)
    # =================================================
    if 'status' in request.GET:
        data_status = request.GET.get('status')
        invoicestatus = get_object_or_404(InvoiceStatus, abbv=data_status)
        invoices = invoices.filter(status=invoicestatus)

    # ================================
    # Paginasi halaman (Version 1.0.0)
    # ================================
    paginator = Paginator(invoices, 20)
    page = request.GET.get('page')
    try:
        invoices = paginator.page(page)
    except PageNotAnInteger:
        invoices = paginator.page(1)
    except EmptyPage:
        invoices = paginator.page(paginator.num_pages)

    data_context = {'invoices': invoices, 'form': form, 'total_count': invoices}
    return render(request, 'apltransaction/invoice/invoiceweb_list.html', 
        data_context)


@trans.atomic
@connecting_brand_required
def invoiceweb_add(request):
    invoicecategory = get_object_or_404(InvoiceCategory, abbv='W')
    invoicestatus = get_object_or_404(InvoiceStatus, abbv='H')
    invoice = Invoice(user=request.user,
                      invoice_number=helper_generate_code(),
                      total=0,
                      category=invoicecategory,
                      status=invoicestatus)

    invoice.save()

    # Hold Target
    # -----------
    hold_target = HoldTarget(user=invoice.user, invoice_number=invoice.invoice_number, state=1)
    hold_target.save()

    return HttpResponseRedirect(reverse('apltransaction:transactiondetailweb_add',
                                        kwargs={'invoice_number':invoice.invoice_number}))


@trans.atomic
def invoiceweb_remove(request, invoice_number):
    """
    fungsi view yang digunakan untuk menghapus invoice berstatus web
    karena alasan tertentu. alasan ini biasanya terjadi
    ketika seorang admin salah membuat invoice atau semacamnya.

    sebelum menghapus invoice, terlebih dahulu sistem akan 
    memeriksa apakah invoice yang mau dihapus memiliki item.
    jika ya, maka kembalikan quantity item-item tersebut ke dalam
    stock article detail (pengembalian stock).
    """
    # ambil data invoice dari invoice number
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
    # periksa apakah invoice punya item pada transaction detail
    if invoice.transactiondetail_set.count() > 0:
        # jika invoice punya item, kembalikan item tersebut
        # ke gudang atau article
        for item in invoice.transactiondetail_set.all():
            try:
                # menggunakan try untuk melempar kesalahan
                # jika item saat ini sudah tidak ada lagi
                # di dalam data article detail.
                article = ArticleDetail.objects.get(code=item.article_code)
                stock_article = article.stock
                # menambahkan stock artikel saat ini dengan stock quantity item
                # yang dipesan.
                article.stock = stock_article + item.quantity
                # menyimpan article kembali
                article.save()
            except:
                pass

    # Hold target
    # -----------
    try:
        hold_target = HoldTarget.objects.get(invoice_number=invoice.invoice_number)
        hold_target.delete()
    except:
        pass

    # setelah pengembalian stock selesai atau bahkan tidak ada
    # yang dikembalikan sama sekali, hapus invoice.
    invoice.delete()
    # kembali ke halaman daftar invoice
    return HttpResponseRedirect(reverse('apltransaction:invoiceweb_list'))


def invoiceweb_print(request, invoice_number):
    """
    Fungsi yang digunakan untuk print invoice berstatus web dalam format pdf.
    fungsi ini akan menampilkan tombol print dan kembali.
    tombol print akan melakukan proses print browser. 
    tombol kembali merujuk ke halaman tambah transaction detail. 
    """
    invoicecategory = get_object_or_404(InvoiceCategory, abbv='W')
    # ambil invoice
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number, category=invoicecategory)
    # ambil transaction detail (item)
    transactiondetails = invoice.transactiondetail_set.all()
    # ambil billing
    billing = invoice.billing_set.all().first()
    # ambil shipping
    shipping = invoice.shipping_set.all().first()
    # ambil brand
    # ambil company/store
    store = Store.objects.all().first()

    # ambil brand terbanyak
    brand = Brand.objects.filter(pk=transactiondetails.first().article_brand_code)
    brand = brand.first()

    data_context = {
        'invoice': invoice, 
        'transactiondetails': transactiondetails, 
        'billing': billing, 
        'shipping': shipping, 
        'store': store,
        'brand': brand}

    return render(request, 'apltransaction/invoice/invoiceweb_print.html', data_context)


@trans.atomic
def invoiceweb_change_status_process(request):
    if request.method == 'POST':
        # ambil semua invoice dalam bentuk list
        invoices_number = request.POST.getlist('_selected_action')
        if request.user.is_superuser:
            # ambil objek invoice
            invoices = Invoice.objects.filter(invoice_number__in=invoices_number,
                category__abbv='W').exclude(
                    Q(transactiondetail=None)| 
                    Q(billing=None)| 
                    Q(shipping=None)| 
                    Q(status__abbv='C'))

        else:
            invoices = Invoice.objects.filter(invoice_number__in=invoices_number,
                category__abbv='W', user=request.user).exclude(Q(transactiondetail=None)| 
                    Q(billing=None)|Q(shipping=None)|Q(status__abbv='C'))

        # memeriksa apakah invoice valid..
        # valid berarti sudah berisi item, shipping dan billing.
        if invoices:
            status = InvoiceStatus.objects.get(abbv='P')
            invoices.update(status=status)
            messages.success(request, 'Invoice successfully changed to ready to process')
        else:
            messages.warning(request, 'You have an invalid invoice')

    return HttpResponseRedirect(reverse('apltransaction:invoiceweb_list'))


@trans.atomic
def invoiceweb_change_status_ready(request):
    if request.method == 'POST':
        # ambil semua invoice dalam bentuk list
        invoices_number = request.POST.getlist('_selected_action')
        if request.user.is_superuser:
            # ambil objek invoice
            invoices = Invoice.objects.filter(invoice_number__in=invoices_number,
                category__abbv='W').exclude(
                    Q(transactiondetail=None)| 
                    Q(billing=None)| 
                    Q(shipping=None)| 
                    Q(status__abbv='C'))

        else:
            invoices = Invoice.objects.filter(invoice_number__in=invoices_number,
                category__abbv='W', user=request.user).exclude(Q(transactiondetail=None)| 
                    Q(billing=None)|Q(shipping=None)|Q(status__abbv='C'))

        # memeriksa apakah invoice valid..
        # valid berarti sudah berisi item, shipping dan billing.
        if invoices:
            status = InvoiceStatus.objects.get(abbv='R')
            invoices.update(status=status)
            messages.success(request, 'Invoice successfully changed to ready to shipping')
        else:
            messages.warning(request, 'You have an invalid invoice')

    return HttpResponseRedirect(reverse('apltransaction:invoiceweb_list'))


@trans.atomic
def invoiceweb_change_status_pending(request):
    if request.method == 'POST':
        # ambil semua invoice dalam bentuk list
        invoices_number = request.POST.getlist('_selected_action')
        if request.user.is_superuser:
            # ambil objek invoice
            invoices = Invoice.objects.filter(invoice_number__in=invoices_number,
                category__abbv='W').exclude(
                    Q(transactiondetail=None)| 
                    Q(billing=None)| 
                    Q(shipping=None)| 
                    Q(status__abbv='C'))

        else:
            invoices = Invoice.objects.filter(invoice_number__in=invoices_number,
                category__abbv='W', user=request.user).exclude(Q(transactiondetail=None)| 
                    Q(billing=None)|Q(shipping=None)|Q(status__abbv='C'))

        # memeriksa apakah invoice valid..
        # valid berarti sudah berisi item, shipping dan billing.
        if invoices:
            status = InvoiceStatus.objects.get(abbv='G')
            invoices.update(status=status)
            messages.success(request, 'Invoice successfully changed to pending')
        else:
            messages.warning(request, 'You have an invalid invoice')

    return HttpResponseRedirect(reverse('apltransaction:invoiceweb_list'))


@trans.atomic
def invoiceweb_change_status_finish(request):
    if request.method == 'POST':
        # ambil semua invoice dalam bentuk list
        invoices_number = request.POST.getlist('_selected_action')
        if request.user.is_superuser:
            # ambil objek invoice
            invoices = Invoice.objects.filter(invoice_number__in=invoices_number,
                category__abbv='W').exclude(
                    Q(transactiondetail=None)| 
                    Q(billing=None)| 
                    Q(shipping=None)| 
                    Q(status__abbv='C'))

        else:
            invoices = Invoice.objects.filter(invoice_number__in=invoices_number,
                category__abbv='W', user=request.user).exclude(Q(transactiondetail=None)| 
                    Q(billing=None)|Q(shipping=None)|Q(status__abbv='C'))

        # memeriksa apakah invoice valid..
        # valid berarti sudah berisi item, shipping dan billing.
        if invoices:
            status = InvoiceStatus.objects.get(abbv='F')
            invoices.update(status=status)
            messages.success(request, 'Invoice successfully changed to finish')
        else:
            messages.warning(request, 'You have an invalid invoice')

    return HttpResponseRedirect(reverse('apltransaction:invoiceweb_list'))


@trans.atomic
def invoiceweb_change_status_cancel(request):
    if request.method == 'POST':
        # ambil semua invoice dalam bentuk list
        invoices_number = request.POST.getlist('_selected_action')
        if request.user.is_superuser:
            # ambil objek invoice
            invoices = Invoice.objects.filter(invoice_number__in=invoices_number,
                category__abbv='W').exclude(
                    transactiondetail=None, 
                    billing=None, 
                    shipping=None)

        else:
            invoices = Invoice.objects.filter(invoice_number__in=invoices_number,
                category__abbv='W', user=request.user).exclude(transactiondetail=None, 
                    billing=None, shipping=None)

        # memeriksa apakah invoice valid..
        # valid berarti sudah berisi item, shipping dan billing.
        if invoices:
            status = InvoiceStatus.objects.get(abbv='C')
            invoices.update(status=status)
            try:
                # fitur cancel barang balik ke gudang tapi
                # tidak bisa di up karena bentrok dengan masalah
                # ketika barang A sudah diambil orang dalam transaksi lain!
                for invoice in invoices:
                    for td in invoice.transactiondetail_set.all():
                        ad = ArticleDetail.objects.get(code=td.article_code)
                        stock = ad.stock
                        ad.stock = td.quantity + stock
                        ad.save()
            except:
                print("error")
                
            messages.success(request, 'Invoice successfully changed to cancel')
        else:
            messages.warning(request, 'You have an invalid invoice')

    return HttpResponseRedirect(reverse('apltransaction:invoiceweb_list'))



@connecting_brand_required
def invoiceweb_print_all(request):
    brand = helper_session_brand_pk(request)
    if request.method == 'POST':
        # ambil semua invoice dalam bentuk list
        invoices_number = request.POST.getlist('_selected_action')

        invoices = Invoice.objects.filter(invoice_number__in=invoices_number, category__abbv='W')

        # mengecek apakah status valid..
        # valid berarti sudah berisi item, shipping dan billing.
        valid = True
        for i in invoices:
            # jika transaction belum di isi data tidak valid
            if i.transactiondetail_set.count() == 0:
                valid = False

            # jika shipping belum di isi data tidak valid
            if i.shipping_set.count() == 0:
                valid = False

            # jika billing belum di isi data tidak valid 
            if i.billing_set.count() == 0:
                valid = False

        # Jika invoice di seleksi
        if invoices:

            # Jika invoice valid
            if valid:
                data_context = {'invoices': invoices, 'brand': brand}
                return render(request, 'apltransaction/invoice/invoiceweb_print_all.html', data_context)
            
            else:
                messages.warning(request, 'Sorry, your invoice not valid. check invoice again !')
        else:
            messages.warning(request, 'Sory, you don\'t selected any item')
    else:
        messages.warning(request, 'Hei {}, fuck youuuu ! this is bad request...you stupid !'.format(request.user))
    
    return HttpResponseRedirect(reverse('apltransaction:invoiceweb_list'))


def invoiceweb_changestatus(request, invoice_number):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
    if request.method == 'POST':
        form = FormInvoiceWebChangeStatus(data=request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Invoice berhasil diubah.')
            kwarg_context = {'invoice_number': invoice_number}
            return HttpResponseRedirect(reverse('apltransaction:transactiondetailweb_add', kwargs=kwarg_context))
    else:
        form = FormInvoiceWebChangeStatus(instance=invoice)
    data_context = {'form': form, 'invoice': invoice}
    return render(request, 'apltransaction/invoice/invoiceweb_changestatus.html', data_context)


def transactiondetailweb_add(request, invoice_number):
    """
    fungsi yang digunakan untuk menambahkan item pada transaksi web.
    item diperoleh dari detail article yang mana nanti item-item
    ini akan disimpan ke dalam transaction detail.
    """
    # ambil invoice
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)

    # ambil semua data item transaction
    transactiondetails = TransactionDetail.objects.filter(invoice=invoice)

    # ambil data billing
    billing = Billing.objects.filter(invoice=invoice).first()

    # ambil data shipping
    shipping = Shipping.objects.filter(invoice=invoice).first()

    try:
        
        if request.method == 'POST':
            form = FormAddTransactionWebDetail(request.POST)
            

            if form.is_valid():

                # tahan penyimpanan data untuk melakukan proses penijauan.
                transactiondetail = form.save(commit=False)

                # Mengambil object "ArticleDetail" berdasarkan field code,
                # field name dari object Article, field price dari object Article
                # dan field name size dari object Size.
                # Langkah ini dilakukan untuk mengecek apakah object "ArticleDetail"
                # benar-benar ada di dalam database. Jika ada, maka valid dan jika
                # tidak ada, maka sistem akan meredirect ke halama 404 Not Found.
                articledetail = get_object_or_404(ArticleDetail,
                                                  code=transactiondetail.article_code,
                                                  article__name=transactiondetail.article_name,
                                                  article__price=transactiondetail.article_price,
                                                  size__name=transactiondetail.article_size)

                # Jika stok dikurang quantity menghasilkan - minus
                if articledetail.stock - transactiondetail.quantity < 0 or transactiondetail.quantity <= 0:
                    # kirim pesan validasi
                    messages.warning(request, 'Stock ordered a very limited number of stocks entirely')
                    
                else:
                    # jika stock tidak minus saat dikurangi oleh quantity atau 
                    # quantity tidak kurang dari atau sama dengan nol
                    transactiondetail.user = request.user
                    transactiondetail.invoice = invoice
                    transactiondetail.article_brand_code = articledetail.brand.pk
                    transactiondetail.article_brand_name = articledetail.brand.name 
                    transactiondetail.article_capitalprice = articledetail.article.capital_price
                    transactiondetail.sub_total = transactiondetail.article_price * transactiondetail.quantity
                    transactiondetail.save()

                    invoice_total = invoice.total + transactiondetail.sub_total
                    invoice.total = invoice_total
                    invoice.save()

                    articledetail.stock = articledetail.stock - transactiondetail.quantity
                    articledetail.save()

                    ##############################################################################################
                    # periksa apakah article detail memiliki discount
                    ##############################################################################################

                    # mengambil objek category invoice dari invoice
                    invoice_category = invoice.category

                    # mengambil objek article dari article detail
                    article = articledetail.article

                    # ambil diskon untuk article saat ini
                    try:
                        discount = Discount.objects.get(place=invoice_category, article=article)
                    except:
                        discount = None

                    # periksa apakah @Article yang dipilih ada diskon
                    if discount:
                        # jika ada, kalikan @Discount.cut_price dengan @TransactionDetail.quantity 
                        # menjadi harga kelipatan diskon
                        kelipatan_diskon = transactiondetail.quantity * discount.cut_price

                        # harga @TransactionDetail.sub_total dengan harga @kelipatan_discount menjadi @harga_potongan_diskon
                        harga_potongan_diskon = transactiondetail.sub_total - kelipatan_diskon

                        # update harga @TransactionDetail.sub_total dengan @harga_potongan_diskon
                        transactiondetail.sub_total = harga_potongan_diskon

                        # update discount code, discount_name dan cut_price pada TransactionDetail saat ini
                        transactiondetail.discount_code = discount.code
                        transactiondetail.discount_name = discount.name
                        transactiondetail.cut_price = discount.cut_price

                        # simpan transaction detail
                        transactiondetail.save()

                        # jumlahkan kembali semua sub total dari transaction detail berdasarkan invoice saat ini.
                        invoice_total = invoice.transactiondetail_set.aggregate(pricing=Sum('sub_total'))

                        # update total invoice dengan total di atas
                        invoice.total = invoice_total.get("pricing")

                        # simpan kembali invoice
                        invoice.save()

                    # Hold Target
                    # -----------
                    try:
                        hold_target = HoldTarget.objects.get(invoice_number=invoice.invoice_number)
                        current_state = hold_target.state
                        hold_target.state = current_state + 1
                        hold_target.save()
                    except:
                        pass

                    return HttpResponseRedirect(reverse('apltransaction:transactiondetailweb_add', kwargs={'invoice_number': invoice_number}))
        else:
            form = FormAddTransactionWebDetail()

    except IntegrityError:
        messages.warning(request, 'Please remove one item same it.')

    data_context = {
            'invoice': invoice, 
            'transactiondetails': transactiondetails, 
            'form': form, 
            'billing': billing, 
            'shipping': shipping}

    return render(request, 'apltransaction/transactiondetail/transactiondetailweb_add.html', data_context)


def transactiondetailweb_remove(request, invoice_number, article_code):
    """
    fungsi yang digunakan untuk menghapus item pada invoice web.
    fungsi ini ada karena jika seorang admin ingin memiliki item
    pada invoice namun jumlah quantity itemnya ingin diganti atau
    item yang dipesan salah.

    setiap item yang dihapus, quantity akan dikembalikan ke stok
    pada detail artikel.
    """

    # ambil invoice
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)

    # ambil transaction detail (item)
    transactiondetail = get_object_or_404(TransactionDetail, article_code=article_code, invoice=invoice)

    # ambil detail article dari code. karena code transaction detail sama dengan
    # code milik article detail 
    articledetail = get_object_or_404(ArticleDetail, code=article_code)

    # ambil quantity
    quantity = transactiondetail.quantity

    # ambil jumlah stock saat ini
    current_stock = articledetail.stock

    # ambil total harga pada invoice
    total = invoice.total

    # set stock invoice yang baru
    articledetail.stock = quantity + current_stock

    # ubah harga pada invoice
    invoice.total = total - transactiondetail.sub_total

    # simpan article detail
    articledetail.save()

    # simpan invoice
    invoice.save()

    # hapus item
    transactiondetail.delete()

    # kembali ke halaman transaction detail web
    data_kwargs = {'invoice_number': invoice_number}
    return HttpResponseRedirect(reverse('apltransaction:transactiondetailweb_add', kwargs=data_kwargs))


