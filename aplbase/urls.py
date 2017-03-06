from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^dashboard\.html$', views.Dashboard.as_view(), name='dashboard'),
]