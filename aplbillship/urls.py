from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^billing/(?P<invoice_number>[\w\-]+)/add/$', views.billing_add, name='billing_add'),
    url(r'^billing/(?P<invoice_number>[\w\-]+)/(?P<code>[\w\-]+)/remove/$', views.billing_remove, name='billing_remove'),
   
    url(r'^shipping/(?P<invoice_number>[\w\-]+)/add/$', views.shipping_add, name='shipping_add'),
    url(r'^shipping/(?P<invoice_number>[\w\-]+)/add/manual/$', views.shipping_add_manual, name='shipping_add_manual'),
    url(r'^shipping/(?P<invoice_number>[\w\-]+)/(?P<code>[\w\-]+)/remove/$', views.shipping_remove, name='shipping_remove'),
    
    url(r'^ajax/province/$', views.ajax_getallprovince, name='ajax_getallprovince'),
    url(r'^ajax/city/(?P<province_id>[\w\-]+)/$', views.ajax_getallcity, name='ajax_getallcity'),
    url(r'^ajax/pack/(?P<invoice_number>[\w\-]+)/(?P<city_id>[\w\-]+)/(?P<vendor>[\w\-]+)/$', views.ajax_getpackage, name='ajax_getpackage'),
]