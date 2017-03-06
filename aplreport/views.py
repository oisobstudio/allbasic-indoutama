import datetime
import csv
import json

from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Count, F
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View

from apltransaction.models import InvoiceStatus, InvoiceCategory
from apltransaction.models import Invoice, TransactionDetail
from aplinventory.models import Article

from .forms import FormReportSaleWebsite
from .forms import FormReportAllSalePerdate
from .forms import FormReportingSaleStore
from .forms import FormReportingSaleWeb
from .forms import FormReportingSaleArticle

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def reporting_sale_store(request):
	if request.method == 'POST':
		form = FormReportingSaleStore(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			from_date = cd['from_date']
			to_date = cd['to_date']

			from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
			to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")

			data_reports = TransactionDetail.objects.filter(
				invoice__invoice_date__range=(from_date, to_date), invoice__category__abbv='S')

			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="{}-{}-{}.csv"'.format(
				"reporting_sale_store", from_date, to_date)

			writer = csv.writer(response)
			writer.writerow(['User', 'Invoice Number', 'Brand', 'Article Code', 'Article Name', 'Size', 'Price', 'Quantity', 'Sub Total'])
			data_csv = []
			
			if data_reports:
				for td in data_reports:
					data_csv.append([
						td.user, 
						td.invoice.invoice_number, 
						td.article_brand_name, 
						td.article_code,
						td.article_name,
						td.article_size,
						td.article_price,
						td.quantity,
						td.sub_total])

				for data in data_csv:
					writer.writerow(data)

				return response

		# TODO: Sending Email automatic after creating CSV

	else:
		form = FormReportingSaleStore()
	return render(request, 'aplreport/reporting_sale_store.html', {'form': form})


def reporting_sale_web(request):
	if request.method == 'POST':
		form = FormReportingSaleWeb(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			from_date = cd['from_date']
			to_date = cd['to_date']

			from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
			to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")

			data_reports = TransactionDetail.objects.filter(
				invoice__invoice_date__range=(from_date, to_date), invoice__category__abbv='W', ).exclude(
				invoice__billing=None, invoice__shipping=None)

			total = data_reports.aggregate(Sum('sub_total'))


			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="{}-{}-{}.csv"'.format(
				"reporting_sale_web", from_date, to_date)

			writer = csv.writer(response)
			writer.writerow(['Penanggung Jawab', 'Status', 'Nomer Invoice', 'Brand', 'Kode Artikel', 'Nama Artikel', 'Ukuran', 'Harga', 'Banyak', 'Sub Total'])
			data_csv = []
			
			if data_reports:
				for td in data_reports:
					data_csv.append([
						td.user, 
						"({}) - {}".format(td.invoice.status.abbv, td.invoice.status.info),
						td.invoice.invoice_number, 
						td.article_brand_name, 
						td.article_code,
						td.article_name,
						td.article_size,
						td.article_price,
						td.quantity,
						td.sub_total])

				for data in data_csv:
					writer.writerow(data)

				print(total)
				writer.writerow(['Total', '', '', '', '', '', '', '', '', total['sub_total__sum']])
				return response

		# TODO: Sending Email automatic after creating CSV

	else:
		form = FormReportingSaleStore()
	return render(request, 'aplreport/reporting_sale_web.html', {'form': form})


def reporting_sale_article(request):
	if request.method == 'POST':
		form = FormReportingSaleArticle(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			from_date = cd['from_date']
			to_date = cd['to_date']

			from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
			to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")

			data_reports = TransactionDetail.objects.filter(invoice__invoice_date__range=(from_date, to_date)).values('article_name', 'user__username').annotate(Count('article_name'))

			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="{}___{}___{}.csv"'.format(
				"reporting_sale_article", from_date, to_date)

			writer = csv.writer(response)
			writer.writerow(['Penanggung Jawab', 'Artikel', 'Total Barang Keluar'])
			data_csv = []
			
			if data_reports:
				for td in data_reports:
					data_csv.append([
						td['user__username'], 
						td['article_name'], 
						td['article_name__count']])

				for data in data_csv:
					writer.writerow(data)

				return response

		# TODO: Sending Email automatic after creating CSV

	else:
		form = FormReportingSaleStore()
	return render(request, 'aplreport/reporting_sale_article.html', {'form': form})


class ReportingStockArticle(View):

	def get(self, request):
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="{}-{}.csv"'.format('reporting_stock_article', datetime.datetime.now())
		dataset = self._make_dataset()
		return self._make_csv(dataset, response)

	def post(self, request):
		return self.get(request)

	def _make_csv(self, dataset, response):
		writer = csv.writer(response)
		writer.writerow(['Brand', 'Article', 'Stock'])
		brand_name = None
		stock_out = 0
		for data in dataset:
			if brand_name:
				if brand_name != data['brand__name']:
					writer.writerow(['','',''])
					writer.writerow(['Brand', 'Article', 'Stock'])
					brand_name = data['brand__name']
					
			else:
				brand_name = data['brand__name']

			writer.writerow([data['brand__name'], data['name'], data['sum_stock']])
			

		return response

	def _make_dataset(self):
		dataset = Article.objects.values('brand__name', 'name').\
							annotate(sum_stock=Sum('articledetail__stock')).\
							order_by('-brand__name')

		return dataset


