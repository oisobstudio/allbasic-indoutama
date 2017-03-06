# Django package import
from django.conf.urls import url

# This app import
from . import views


urlpatterns = [
    # Store url
    url(r'^store\.html$', views.StoreDetail.as_view(), name='store_detail'),
    url(r'^store/add\.html$', views.StoreAdd.as_view(), name='store_add'),
    url(r'^store/(?P<store_pk>[0-9]+)/change\.html$', views.StoreChange.as_view(), name='store_change'),

    # Brand url
    url(r'^brand\.html$', views.BrandList.as_view(), name='brand_list'),
    url(r'^brand/add\.html$', views.BrandAdd.as_view(), name='brand_add'),
    url(r'^brand/(?P<brand_pk>[0-9]+)/change\.html$', views.BrandChange.as_view(), name='brand_change'),
    url(r'^brand/(?P<brand_pk>[0-9]+)/remove\.html$', views.BrandRemove.as_view(), name='brand_remove'),
    url(r'^brand/(?P<brand_pk>[0-9]+)/connect\.html$', views.BrandConnect.as_view(), name='brand_connect'),
]