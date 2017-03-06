from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^discount\.html$', views.DiscountList.as_view(), name='DiscountList'),
	url(r'^discount/add\.html$', views.DiscountAdd.as_view(), name='DiscountAdd'),
	url(r'^discount/(?P<discount_code>[\w\-]+)/change\.html$', views.DiscountChange.as_view(), name='DiscountChange'),
	url(r'^discount/(?P<discount_code>[\w\-]+)/remove\.html$', views.DiscountRemove.as_view(), name='DiscountRemove'),
]
