from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from aplhelper.views import helper_generate_code

from .models import Discount
from .forms import FormDiscountAdd
from .forms import FormDiscountChange


class DiscountList(View):
	template = 'aplpromotion/discount/discount_list.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(DiscountList, self).dispatch(*args, **kwargs)

	def get(self, request):
		discounts = Discount.objects.all()	
		data_context = {'discounts': discounts}
		return render(request, self.template, data_context)

	def post(self, request):
		return self.get(request)


class DiscountAdd(View):
	form_discount_add = FormDiscountAdd
	template = 'aplpromotion/discount/discount_add.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(DiscountAdd, self).dispatch(*args, **kwargs)

	def get(self, request):
		form = self.form_discount_add()

		data_context = {'form': form}
		return render(request, self.template, data_context)

	def post(self, request):
		form = self.form_discount_add(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.code = "DCT-" + helper_generate_code()
			instance.save()
			return HttpResponseRedirect(reverse('aplpromotion:DiscountList'))

		data_context = {'form': form}
		return render(request, self.template, data_context)


class DiscountChange(View):
	form_discount_change = FormDiscountChange
	template = 'aplpromotion/discount/discount_change.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(DiscountChange, self).dispatch(*args, **kwargs)

	def get(self, request, discount_code):
		discount = get_object_or_404(Discount, code=discount_code) 
		form = self.form_discount_change(instance=discount)

		data_context = {'form': form}
		return render(request, self.template, data_context)

	def post(self, request, discount_code):
		discount = get_object_or_404(Discount, code=discount_code)
		form = self.form_discount_change(instance=discount, data=request.POST)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('aplpromotion:DiscountList'))

		data_context = {'form': form}
		return render(request, self.template, data_context)


class DiscountRemove(View):

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(DiscountRemove, self).dispatch(*args, **kwargs)

	def get(self, request, discount_code):
		discount = get_object_or_404(Discount, code=discount_code)
		discount.delete()
		return HttpResponseRedirect(reverse('aplpromotion:DiscountList'))

	def post(self, request, discount_code):
		return self.get(request, discount_code)




