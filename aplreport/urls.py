from django.conf.urls import url
from . import views


urlpatterns = [

	url(r'^stock/out/article/web\.html$', views.report_stock_out_article_web, name='report_stock_out_article_web'),
	url(r'^sale/web\.html$', views.report_sale_web, name='report_sale_web'),
	url(r'^all/sale/perdate\.html$', views.report_all_sale_perdate, name='report_all_sale_perdate'),

	url(r'^reporting/sale/store\.html$', views.reporting_sale_store, name='reporting_sale_store'),
	url(r'^reporting/sale/web\.html$', views.reporting_sale_web, name='reporting_sale_web'),
	url(r'^reporting/sale/article\.html$', views.reporting_sale_article, name='reporting_sale_article'),
	url(r'^reporting/stock/article\.html$', views.ReportingStockArticle.as_view(), name='ReportingStockArticle'),
	

]