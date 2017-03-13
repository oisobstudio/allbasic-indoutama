import json

from django.views.generic import View
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder


# ================
# Inner app module
# ================
from .models import Invoice
from .models import TransactionDetail 
from .models import InvoiceCategory
from .models import InvoiceStatus


class AjaxInvoiceWebList(View):

	def post(self, request):
		# Ambil semua data invoice yang valid
		invoices = self._datatables(request)
		return HttpResponse(json.dumps(invoices, cls=DjangoJSONEncoder), content_type='application/json')
		
	def _datatables(self, request):
		datatables = request.POST
		# Ambil draw
		draw = int(datatables.get('draw'))
		# Ambil start
		start = int(datatables.get('start'))
		# Ambil length (limit)
		length = int(datatables.get('length'))
		# Ambil data search
		search = datatables.get('search[value]')
		# Set record total
		records_total = Invoice.objects.all().exclude(Q(transactiondetail=None)|Q(shipping=None)|Q(billing=None)).count()
		# Set records filtered
		records_filtered = records_total
		# Ambil semua invoice yang valid
		invoices = Invoice.objects.all().exclude(Q(transactiondetail=None)|Q(shipping=None)|Q(billing=None))

		if search:
			invoices = Invoice.objects.filter(
					Q(invoice_number__icontains=search)|
					Q(user__username__icontains=search)|
					Q(category__info__icontains=search)|
					Q(status__info__icontains=search)
				).exclude(Q(transactiondetail=None)|Q(shipping=None)|Q(billing=None))
			records_total = invoices.count()
			records_filtered = records_total

		# Atur paginator
		paginator = Paginator(invoices, length)

		try:
			object_list = paginator.page(draw).object_list
		except PageNotAnInteger:
			object_list = paginator.page(draw).object_list
		except EmptyPage:
			object_list = paginator.page(paginator.num_pages).object_list


		data = [
			{
				'user': inv.user.username,
				'invoice_number': inv.invoice_number,
				'date_transaction': inv.invoice_date,
				'total_price': inv.total,
				'category': inv.category.info,
				'status': inv.status.info
			} for inv in object_list
		]

		return {
			'draw': draw,
			'recordsTotal': records_total,
			'recordsFiltered': records_filtered,
			'data': data,
		}
		

