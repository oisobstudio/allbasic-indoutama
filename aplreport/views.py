import datetime
import csv
import json

from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Count, F, Q, Avg
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View

from apltransaction.models import InvoiceStatus, InvoiceCategory
from apltransaction.models import Invoice, TransactionDetail
from aplinventory.models import Article

from .forms import FormReportSalesGrow
from .forms import FormReportSalesNet
from .forms import FormReportInvoice

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from dataresource.models import HoldTarget

class ReportSalesGrow(View):
	"""Laporan penjualan kotor dalam periode (no hold). 
	(ada average gross daily + harganya dipisahin sama harga total shipping). 
	harga ongkir juga digabung."""
	form_report_sales_grow = FormReportSalesGrow
	template = 'aplreport/report_sales_grow.html'
	context = {}

	def get(self, request):
		form = self.form_report_sales_grow()
		self.context['form'] = form
		return render(request, self.template, self.context)

	def post(self, request):
		form = self.form_report_sales_grow(request.POST)
		if form.is_valid():
			cd = form.cleaned_data

			# Ambil tanggal from dan to
			from_date = datetime.datetime.strptime(cd['from_date'], "%Y-%m-%d")
			to_date = datetime.datetime.strptime(cd['to_date'], "%Y-%m-%d")

			# Hitung data gross
			data = self._calc_grow(from_date, to_date)

			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="{}____{}-{}.csv"'.format(
						"Report Sales Grow", from_date, to_date)

			# csv bagian header
			writer = csv.writer(response)

			# Tulis csv untuk From dan To 
			writer.writerow(['From', '', from_date])
			writer.writerow(['To', '', to_date])

			# Tulis csv untuk Total Gros
			writer.writerow(['Total Gross', '', data['total_gross']])
			writer.writerow(['Average', '', data['total_avg']])
			writer.writerow([])

			# Tulis csv Date, Gross dan Shipping
			writer.writerow(['Date', 'Gross', 'Shipping'])

			for sales in data['sales_gross']:
				row = [sales['invoice_date'], sales['total_gross'], sales['total_gross_shipping']]
				writer.writerow(row)

			return response

		self.context['form'] = form
		return render(request, self.template, self.context)

	def _calc_grow(self, from_date, to_date):
		gross = Invoice.objects.filter(
			category__abbv='W', 
			invoice_date__range=(from_date, to_date))\
		.exclude(
			transactiondetail=None,
			billing=None,
			shipping=None,
			status__abbv='H'
		)


		# hitung total gross keseluruhan
		total_gross = gross.values('invoice_date')\
			.aggregate(total_gross=Sum("total"), total_gross_shipping=Sum("shipping__price"))
		total_gross = total_gross['total_gross'] + total_gross['total_gross_shipping']
		
		# Hitung rata-rata
		total_avg = gross.values('invoice_date').annotate(total_gross=Sum('total'), total_gross_shipping=Sum('shipping__price'))\
			.aggregate(total_avg=Avg("total_gross"), total_shipping_avg=Avg('total_gross_shipping'))
		print(total_avg)
		total_avg = total_avg['total_avg'] + total_avg['total_shipping_avg']

		# Hitung penjualan kotor
		sales_gross = gross.values('invoice_date').annotate(total_gross=Sum('total'), total_gross_shipping=Sum('shipping__price'))

		data = {
			'total_gross': total_gross,
			'total_avg': total_avg,
			'sales_gross': sales_gross
		}

		return data


class ReportSalesNet(View):
	"""Laporan Penjualan Bersih (no hold). 
	(ada average gross daily + harganya dipisahin sama harga total shipping). 
	harga ongkir tidak digabung. soalnya harga net sale itu harga total 
	invoice yang tidak dihitung dengan harga ongkir."""
	form_report_sales_grow = FormReportSalesNet
	template = 'aplreport/report_sales_net.html'
	context = {}

	def get(self, request):
		form = self.form_report_sales_grow()
		self.context['form'] = form
		return render(request, self.template, self.context)

	def post(self, request):
		form = self.form_report_sales_grow(request.POST)
		if form.is_valid():
			cd = form.cleaned_data

			# Ambil tanggal from dan to
			from_date = datetime.datetime.strptime(cd['from_date'], "%Y-%m-%d")
			to_date = datetime.datetime.strptime(cd['to_date'], "%Y-%m-%d")

			# Hitung data gross
			data = self._calc_net(from_date, to_date)

			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="{}____{}-{}.csv"'.format(
						"Report Sales Grow", from_date, to_date)

			# csv bagian header
			writer = csv.writer(response)

			# Tulis csv untuk From dan To 
			writer.writerow(['From', '', from_date])
			writer.writerow(['To', '', to_date])

			# Tulis csv untuk Total Gros
			writer.writerow(['Total Net', '', data['total_net']])
			writer.writerow(['Average', '', data['total_avg']])
			writer.writerow([])

			# Tulis csv Date, Gross dan Shipping
			writer.writerow(['Date', 'Net', 'Shipping'])

			for sales in data['sales_net']:
				row = [sales['invoice_date'], sales['total_net'], sales['total_shipping']]
				writer.writerow(row)

			return response

		self.context['form'] = form
		return render(request, self.template, self.context)

	def _calc_net(self, from_date, to_date):
		nets = Invoice.objects.filter(
			category__abbv='W', 
			invoice_date__range=(from_date, to_date))\
		.exclude(
			transactiondetail=None,
			billing=None,
			shipping=None,
			status__abbv='H'
		)

		# hitung total gross keseluruhan
		total_net = nets.values('invoice_date')\
			.aggregate(total_net=Sum("total"))
		total_net = total_net['total_net']
		
		# Hitung rata-rata
		total_avg = nets.values('invoice_date').annotate(total_net=Sum('total'))\
			.aggregate(total_avg=Avg("total_net"))
		total_avg = total_avg['total_avg']

		# Hitung penjualan kotor
		sales_net = nets.values('invoice_date').annotate(total_net=Sum('total'), total_shipping=Sum('shipping__price'))

		data = {
			'total_net': total_net,
			'total_avg': total_avg,
			'sales_net': sales_net
		}

		return data


class ReportInvoice(View):
	'''Laporan invoice yang masuk (not hold).'''
	form_report_invoice = FormReportInvoice
	template = 'aplreport/report_invoice.html'
	context = {}

	def get(self, request):
		form = self.form_report_invoice()
		self.context['form'] = form
		return render(request, self.template, self.context)

	def post(self, request):
		form = self.form_report_invoice(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			# Ambil tanggal mulai sampai tanggal akhir
			from_date = datetime.datetime.strptime(cd['from_date'], "%Y-%m-%d")
			to_date = datetime.datetime.strptime(cd['to_date'], "%Y-%m-%d")

			# Hitung banyak invoice yang dikelompokan berdasarkan tanggal...
			data = self._calc(from_date, to_date)

			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="{}____{}-{}.csv"'.format(
						"Report Invoice", from_date, to_date)
			writer = csv.writer(response)

			# Tulis csv untuk From dan To 
			writer.writerow(['From', from_date])
			writer.writerow(['To', to_date])

			# Tulis csv untuk Total Gros
			writer.writerow(['Total Invoice', data['total_invoices_perdate']])
			writer.writerow([])

			# Tulis csv Date, Gross dan Shipping
			writer.writerow(['Date', 'Total Invoice per Date'])

			for sales in data['invoices_perdate']:
				row = [sales['invoice_date'], sales['total_invoice']]
				writer.writerow(row)

			return response

		self.context['form'] = form
		return render(request, self.template, self.context)

	def _calc(self, from_date, to_date):
		invoices = Invoice.objects.filter(category__abbv='W', invoice_date__range=(from_date, to_date))\
			.exclude(
				transactiondetail=None,
				billing=None,
				shipping=None,
			)

		# Hitung jumlah invoice yang dibuat yang dikelompokan berdasarkan tanggalnya
		invoices_perdate = invoices.values('invoice_date').annotate(total_invoice=Count('invoice_number'))
		total_invoices_perdate = invoices.aggregate(total_invoice=Count('invoice_number'))

		return {
			'invoices_perdate': invoices_perdate,
			'total_invoices_perdate': total_invoices_perdate['total_invoice']
		}


class ReportHoldTarget(View):

	def get(self, request):
		param = request.GET.get('username')
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format("Report Admin Target")
		if param:
			writer = csv.writer(response)

			hold_target = HoldTarget.objects.filter(user__username=param).first()
			total_target = HoldTarget.objects.filter(user__username=param, state=4).aggregate(total_target=Count('record_date'))
			writer.writerow(['Admin', param])
			writer.writerow(['Total Semua Target Pencapaian', total_target['total_target']])
			writer.writerow(['',''])
			writer.writerow(['Per Tanggal', 'Jumlah Target yang Dicapai'])

			dataset = self._calc(hold_target.user)

			for data in dataset:
				writer.writerow([data['record_date'], data['total_target']])

			return response
		else:
			return HttpResponse()

	def _calc(self, user):
		dataset = HoldTarget.objects.filter(user=user, state=4).values('record_date').annotate(total_target=Count('record_date'))
		return dataset


class ReportArticle(View):
	"""Laporan Barapa Artikel yang keluar (not hold)."""

	def get(self, request):
		pass

	def post(self, request):
		pass


class ReportShipping(View):
	"""Laporan ongkir (no hold)."""

	def get(self, request):
		pass

	def post(self, request):
		pass

