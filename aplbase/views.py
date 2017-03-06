from django.shortcuts import render
from django.db.models import Sum, Count, Q
from django.views.generic import View

import datetime
import json
from aplinventory.models import Article, ArticleDetail
from apltransaction.models import Invoice, TransactionDetail


class Dashboard(View):
	template = 'aplbase/dashboard.html'
	data_context = {}

	def get(self, request):
		self._dataset_total_article_by_brand()
		self._dataset_total_article_by_size()
		return render(request, self.template, self.data_context)

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




