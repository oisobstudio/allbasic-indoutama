from django.shortcuts import render
from django.db.models import When, F, Q, Sum, Count, IntegerField, Case
from django.views.generic import View

import datetime
import json
from aplinventory.models import Article, ArticleDetail
from apltransaction.models import Invoice, TransactionDetail

from dataresource.models import HoldTarget

class Dashboard(View):
	template = 'aplbase/dashboard.html'
	data_context = {}

	def get(self, request):
		self._dataset_total_article_by_brand()
		self._dataset_total_article_by_size()
		self._dataset_sale_admin_performance()
		self._dataset_informasi_invalid_invoice()
		self._dataset_hold_target()

		return render(request, self.template, self.data_context)

	def _dataset_hold_target(self):
		# Hold Target
		# -----------
		data = HoldTarget.objects.filter(state=4).values('user__username').annotate(total_target=Count('record_date'))
		self.data_context['dataset_hold_target'] = data

	def _dataset_total_article_by_brand(self):
		total_article_by_brand = ArticleDetail.objects.values_list('brand__name').\
									annotate(sum_stock=Sum('stock'))

		# konversi data menjadi format yang didukung chart-js
		dataset_total_article_by_brand = {}

		# ubah dataset
		dataset_total_article_by_brand['brand_name'],\
		dataset_total_article_by_brand['sum_stock'] = [list(i) for i in list(zip(*total_article_by_brand))]

		self.data_context['dataset_total_article_by_brand'] = json.dumps(dataset_total_article_by_brand)

	def _dataset_total_article_by_size(self):
		total_article_in_brand_size = ArticleDetail.objects.values_list('brand__name', 'article__name', 'size__name').\
										annotate(sum_stock=Sum('stock'))

		dataset_total_article_in_brand_size = list(total_article_in_brand_size)

		self.data_context['dataset_total_article_in_brand_size'] = json.dumps(dataset_total_article_in_brand_size)

	def _dataset_sale_admin_performance(self):

		total_invoice_per_status = TransactionDetail.objects.exclude(Q(invoice__billing=None)|Q(invoice__shipping=None)).values('user__username').annotate(
			hold=Sum(
				Case(When(invoice__status__abbv='H', then=1), output_field=IntegerField())
			),
			process=Sum(
				Case(When(invoice__status__abbv='P', then=1), output_field=IntegerField())
			),
			ready=Sum(
				Case(When(invoice__status__abbv='R', then=1), output_field=IntegerField())
			),
			pending=Sum(
				Case(When(invoice__status__abbv='G', then=1), output_field=IntegerField())
			),
			cancel=Sum(
				Case(When(invoice__status__abbv='C', then=1), output_field=IntegerField())
			),
			finish=Sum(
				Case(When(invoice__status__abbv='F', then=1), output_field=IntegerField())
			)
		)

		self.data_context['dataset_sale_admin_performance'] = total_invoice_per_status


	def _dataset_informasi_invalid_invoice(self):
		data = Invoice.objects.filter(Q(billing=None)|Q(shipping=None)|Q(transactiondetail=None)).values('user__username').\
				annotate(Count('user__username'))
		self.data_context['dataset_informasi_invalid_invoice'] = data




