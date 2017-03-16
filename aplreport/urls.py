from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^reporting/sales/grow\.html$', views.ReportSalesGrow.as_view(), name='report_sales_grow'),
	url(r'^reporting/sales/net\.html$', views.ReportSalesNet.as_view(), name='report_sales_net'),
	url(r'^reporting/invoice\.html$', views.ReportInvoice.as_view(), name='report_invoice'),
	url(r'^reporting/hold/target\.html$', views.ReportHoldTarget.as_view(), name='report_hold_target'),
]

