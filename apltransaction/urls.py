from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^ajax/invoice/remove/hold/invalid\.html', views.ajax_invoice_remove_hold_and_invalid, name='ajax_invoice_remove_hold_and_invalid'),

    # Invoice Store URL
    url(r'^invoice/store\.html$', views.invoicestore_list, name='invoicestore_list'),
    url(r'^invoice/store/add\.html$', views.invoicestore_add, name='invoicestore_add'),
    url(r'^invoice/store/(?P<invoice_number>[\w\-]+)/print\.html$', views.invoicestore_print, name='invoicestore_print'),
    url(r'^invoice/store/(?P<invoice_number>[\w\-]+)/remove\.html$', views.invoicestore_remove, name='invoicestore_remove'),
    
    # Transaction Store URL
    url(r'^transdetail/store/(?P<invoice_number>[\w\-]+)/add\.html$', views.transactiondetailstore_add, name='transactiondetailstore_add'),
    url(r'^transdetail/store/(?P<invoice_number>[\w\-]+)/(?P<article_code>[\w\-]+)/remove\.html$', views.transactiondetailstore_remove, name='transactiondetailstore_remove'),

    # Invoice Web URL
    url(r'^invoice/web\.html$', views.invoiceweb_list, name='invoiceweb_list'),
    url(r'^invoice/web/add\.html$', views.invoiceweb_add, name='invoiceweb_add'),
    url(r'^invoice/web/(?P<invoice_number>[\w\-]+)/remove\.html$', views.invoiceweb_remove, name='invoiceweb_remove'),
    url(r'^invoice/web/(?P<invoice_number>[\w\-]+)/print\.html$', views.invoiceweb_print, name='invoiceweb_print'),
    url(r'^invoice/web/(?P<invoice_number>[\w\-]+)/changestatus\.html$', views.invoiceweb_changestatus, name='invoiceweb_changestatus'),
    url(r'^invoice/web/print/all\.html$', views.invoiceweb_print_all, name="invoiceweb_print_all"),
    url(r'^invoice/web/change/status/process\.html', views.invoiceweb_change_status_process, name='invoiceweb_change_status_process'),
    url(r'^invoice/web/change/status/ready\.html', views.invoiceweb_change_status_ready, name="invoiceweb_change_status_ready"),
    url(r'^invoice/web/change/status/pending\.html', views.invoiceweb_change_status_pending, name="invoiceweb_change_status_pending"),
    url(r'^invoice/web/change/status/finish\.html', views.invoiceweb_change_status_finish, name="invoiceweb_change_status_finish"),
    url(r'^invoice/web/change/status/cancel\.html', views.invoiceweb_change_status_cancel, name="invoiceweb_change_status_cancel"),
    
    # ==========================
    # Transaction Detail Web URL
    # ==========================
    url(r'^transdetail/web/(?P<invoice_number>[\w\-]+)/add\.html$', views.transactiondetailweb_add, name='transactiondetailweb_add'),
    url(r'^transdetail/web/(?P<invoice_number>[\w\-]+)/(?P<article_code>[\w\-]+)/remove\.html$', views.transactiondetailweb_remove, name='transactiondetailweb_remove'),


]