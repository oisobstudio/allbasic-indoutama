from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.account_login, name='account_login'),
	url(r'^logout\.html$', views.account_logout, name='account_logout'),
]