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
				invoice__invoice_date__range=(from_date, to_date), invoice__category__abbv='W').exclude(invoice__billing=None)

			total = data_reports.aggregate(Sum('sub_total'))


			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="{}-{}-{}.csv"'.format(
				"reporting_sale_web", from_date, to_date)

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

				print(total)
				writer.writerow(['Total', '', '', '', '', '', '', '', total['sub_total__sum']])
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

			data_reports = TransactionDetail.objects.values('article_name').annotate(Count('article_name'))

			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="{}___{}___{}.csv"'.format(
				"reporting_sale_article", from_date, to_date)

			writer = csv.writer(response)
			writer.writerow(['Article', 'Total Out'])
			data_csv = []
			
			if data_reports:
				for td in data_reports:
					data_csv.append([
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
	template = 'aplreport/ReportingStock.html'

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
		for data in dataset:
			writer.writerow(list(data.values()))

		return response

	def _make_dataset(self):
		dataset = Article.objects.values('brand__name', 'name').\
							annotate(sum_stock=Sum('articledetail__stock')).\
							order_by('-brand__name')

		return dataset



def reporting_stock_brand(request):
	pass




def ajax_reporting_omzet(request):
	pass


def ajax_reporting_admin_performance(request):
	pass





def ajax_reporting_invoice_hold(request):
	pass


def ajax_reporting_invoice_process(request):
	pass



def report_sale_web(request):
	data_reportsalewebsite = None
	data_total = []
	invoicecategory = get_object_or_404(InvoiceCategory, abbv='W')
	invoicestatus = get_object_or_404(InvoiceStatus, abbv='F')
	if request.method == 'POST':
		form = FormReportSaleWebsite(request.POST)

		if form.is_valid():
			cd = form.cleaned_data
			from_date = cd['from_date']
			to_date = cd['to_date']
			from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
			to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")
			fromdate, todate = from_date, to_date

			data_reportsalewebsite = TransactionDetail.objects.filter(
				invoice__invoice_date__range=(from_date, to_date))

			# nanti tolong diganti menjadi W
			data_reportsalewebsite = data_reportsalewebsite.filter(
				invoice__status=invoicestatus, invoice__category=invoicecategory) 

			data_reportsalewebsite = data_reportsalewebsite.values(
				'invoice__invoice_number',
				'invoice__invoice_date',
				'article_code', 
				'article_name', 
				'article_size', 
				'article_price', 
				'article_capitalprice', 
				'quantity', 
				'sub_total')

			data_total = sum([i['sub_total'] for i in data_reportsalewebsite])
			print(data_total)
	else:
		form = FormReportSaleWebsite()

	data_context = {
		'data_reportsalewebsite': data_reportsalewebsite, 
		'form': form, 
		'data_total': data_total
	}

	return render(request, 'aplreport/report_sale_web.html', data_context)


def report_sale_store(request):
	data_reportsalewebsite = None
	data_total = []
	invoicecategory = get_object_or_404(InvoiceCategory, abbv='W')
	invoicestatus = get_object_or_404(InvoiceStatus, abbv='F')
	if request.method == 'POST':
		form = FormReportSaleWebsite(request.POST)

		if form.is_valid():
			cd = form.cleaned_data
			from_date = cd['from_date']
			to_date = cd['to_date']
			from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
			to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")
			fromdate, todate = from_date, to_date

			data_reportsalewebsite = TransactionDetail.objects.filter(
				invoice__invoice_date__range=(from_date, to_date))

			# nanti tolong diganti menjadi W
			data_reportsalewebsite = data_reportsalewebsite.filter(
				invoice__status=invoicestatus, invoice__category=invoicecategory) 

			data_reportsalewebsite = data_reportsalewebsite.values(
				'invoice__invoice_number',
				'invoice__invoice_date',
				'article_code', 
				'article_name', 
				'article_size', 
				'article_price', 
				'article_capitalprice', 
				'quantity', 
				'sub_total')

			data_total = sum([i['sub_total'] for i in data_reportsalewebsite])
			print(data_total)
	else:
		form = FormReportSaleWebsite()

	data_context = {
		'data_reportsalewebsite': data_reportsalewebsite, 
		'form': form, 
		'data_total': data_total
	}

	return render(request, 'aplreport/report_sale_web.html', data_context)


def report_stock_out_article_web(request):
	data_reportsalewebsite = None
	data_total = []
	invoicecategory = get_object_or_404(InvoiceCategory, abbv='W')
	invoicestatus = get_object_or_404(InvoiceStatus, abbv='F')

	if request.method == 'POST':
		form = FormReportSaleWebsite(request.POST)

		if form.is_valid():
			cd = form.cleaned_data
			from_date = cd['from_date']
			to_date = cd['to_date']
			from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
			to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")
			fromdate, todate = from_date, to_date

			data_reportsalewebsite = TransactionDetail.objects.filter(
				invoice__invoice_date__range=(from_date, to_date))

			data_reportsalewebsite = data_reportsalewebsite.filter(
				invoice__status=invoicestatus, invoice__category=invoicecategory)

			data_reportsalewebsite = data_reportsalewebsite.values(
				'article_code',
				'article_name', 
				'article_size', 
				'article_price')\
			.annotate(total_quantity=Sum('quantity'))

			data_total = TransactionDetail.objects.filter(
				invoice__invoice_date__range=(from_date, to_date), 
				invoice__status=invoicestatus, invoice__category=invoicecategory)\
			.aggregate(Sum('quantity'))
	else:
		form = FormReportSaleWebsite()
	
	data_context = {
		'data_reportsalewebsite': data_reportsalewebsite, 
		'form': form, 
		'data_total': data_total
	}

	return render(request, 'aplreport/report_stock_out_article_web.html', 
		data_context)


def report_all_sale_perdate(request):
	invoicestatus = get_object_or_404(InvoiceStatus, abbv='F')
	data_reports = TransactionDetail.objects.filter(invoice__status=invoicestatus)
	from_date = ''
	to_date = ''
	page = request.GET.get('page')

	if 'from_date' and 'to_date' in request.GET:
		form = FormReportAllSalePerdate(request.GET)

		if form.is_valid():
			cd = form.cleaned_data
			from_date = cd['from_date']
			to_date = cd['to_date']
			data_reports = TransactionDetail.objects.filter(
				invoice__invoice_date__range=(from_date, to_date), invoice__status=invoicestatus)

			if request.GET.get('print'):
				data_context = {
					'data_reports': data_reports,
					'from_date': from_date,
					'to_date': to_date
				}
				return render(request, 'aplreport/report_all_sale_perdate_print.html', data_context)
			
			if request.GET.get('csv'):
				response = HttpResponse(content_type='text/csv')
				filename = "report-csv-{}".format(datetime.datetime.now())
				response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
				writer = csv.writer(response)
				writer.writerow([
					'USER', 			# 1
					'BRAND',			# 2
					'INVOICE NUMBER', 
					'INVOICE DATE', 
					'ARTICLE CODE', 
					'ARTICLE NAME',
					'ARTICLE SIZE',
					'ARTICLE PRICE',
					'CAPITAL PRICE',
					'QUANTITY',
					'TOTAL'])

				for transdet in data_reports:
					writer.writerow([
						transdet.user,
						transdet.article_brand_name,
						"{}".format(transdet.invoice.invoice_number),
						transdet.invoice.invoice_date,
						transdet.article_code,
						transdet.article_name,
						transdet.article_size,
						transdet.article_price,
						transdet.article_capitalprice,
						transdet.quantity,
						transdet.sub_total
						])

				return response

			if request.GET.get('email'):
				from django.core.mail import EmailMultiAlternatives

				subject, from_email, to = 'Report Sale', 'yanwarsolah@gmail.com', 'hwijayaa666@gmail.com'
				text_content = 'Report Sale All'
				html_content = "<table border=1>"
				html_content += """
					<tr>
						<th>USER</th>
						<th>BRAND</th>
						<th>INVOICE NUMBER</th>
						<th>INVOICE DATE</th>
						<th>ARTICLE CODE</th>
						<th>ARTICLE NAME</th>
						<th>ARTICLE SIZE</th>
						<th>ARTICLE PRICE</th>
						<th>CAPITAL PRICE</th>
						<th>QUANTITY</th>
						<th>TOTAL</th>
					</tr>
				"""
				for transdet in data_reports:
					html_content += """
						<tr>
							<td>{}</td>
							<td>{}</td>
							<td>{}</td>
							<td>{}</td>
							<td>{}</td>
							<td>{}</td>
							<td>{}</td>
							<td>{}</td>
							<td>{}</td>
							<td>{}</td>
							<td>{}</td>
						</tr>
					""".format(
						transdet.user,
						transdet.article_brand_name,
						"{}".format(transdet.invoice.invoice_number),
						transdet.invoice.invoice_date,
						transdet.article_code,
						transdet.article_name,
						transdet.article_size,
						transdet.article_price,
						transdet.article_capitalprice,
						transdet.quantity,
						transdet.sub_total
					)

				html_content += "</table>"
				msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
				msg.attach_alternative(html_content, "text/html")
				msg.send()
				
	else:
		form = FormReportAllSalePerdate()

	paginator = Paginator(data_reports, 10) # 10 Page show in page
	try:
		data_reports = paginator.page(page)
	except PageNotAnInteger:
		data_reports = paginator.page(1)
	except EmptyPage:
		data_reports = paginator.page(paginator.num_pages)

	data_context = {
		'data_reports': data_reports, 
		'form': form, 
		'from_date': from_date,
		'to_date': to_date
	}

	return render(request, 'aplreport/report_all_sale_perdate.html', data_context)


# def report_all_sale_perdate_print(request):
# 	data_reports = TransactionDetail.objects.all()
# 	invoicestatus = get_object_or_404(InvoiceStatus, abbv='F')

# 	if 'from_date' and 'to_date' in request.GET:
# 		form = FormReportAllSalePerdate(request.GET)

# 		if form.is_valid():
# 			cd = form.cleaned_data
# 			from_date = cd['from_date']
# 			to_date = cd['to_date']
# 			data_reports = TransactionDetail.objects.filter(
# 				invoice__invoice_date__range=(from_date, to_date), invoice__status=invoicestatus)
# 	else:
# 		form = FormReportAllSalePerdate()

# 	data_context = {
# 		'data_reports': data_reports, 
# 	}

