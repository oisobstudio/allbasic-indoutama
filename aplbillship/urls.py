from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^billing/(?P<invoice_number>[\w\-]+)/add\.html$', views.billing_add, name='billing_add'),
    url(r'^billing/(?P<invoice_number>[\w\-]+)/(?P<code>[\w\-]+)/remove\.html$', views.billing_remove, name='billing_remove'),

    url(r'^shipping/(?P<invoice_number>[\w\-]+)/add\.html$', views.shipping_add, name='shipping_add'),
    url(r'^shipping/(?P<invoice_number>[\w\-]+)/(?P<code>[\w\-]+)/remove\.html$', views.shipping_remove, name='shipping_remove'),
]