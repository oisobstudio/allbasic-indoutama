# Django package import
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.decorators import method_decorator
# Other app import
from aplhelper.views import helper_generate_code
# This app import
from .models import Brand
from .models import Profile
from .models import Store
from .forms import FormStoreAdd
from .forms import FormStoreChange
from .forms import FormBrandAdd
from .forms import FormBrandChange


class StoreDetail(View):
    template = 'apldistro/store/store_detail.html'
    data_context = {}

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StoreDetail, self).dispatch(*args, **kwargs)

    def get(self, request):
        store = Store.objects.all().first()
        self.data_context['store'] = store
        return render(request, self.template, self.data_context)


class StoreAdd(View):
    form_store_add = FormStoreAdd
    template = 'apldistro/store/store_add.html'
    data_context = {}

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StoreAdd, self).dispatch(*args, **kwargs)

    def get(self, request):
        form = self.form_store_add()
        self.data_context['form'] = form
        return render(request, self.template, self.data_context)

    def post(self, request):
        form = self.form_store_add(data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Store successfully added')
            return HttpResponseRedirect(reverse('apldistro:store_detail'))

        self.data_context['form'] = form
        return render(request, self.template, self.data_context)


class StoreChange(View):
    form_store_change = FormStoreChange
    template = 'apldistro/store/store_change.html'
    data_context = {}

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StoreChange, self).dispatch(*args, **kwargs)

    def get(self, request, store_pk):
        store = get_object_or_404(Store, pk=store_pk)
        form = self.form_store_change(instance=store)
        self.data_context['form'] = form
        return render(request, self.template, self.data_context)

    def post(self, request, store_pk):
        store = get_object_or_404(Store, pk=store_pk)
        form = self.form_store_change(instance=store, data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Store successfully changed')
            return HttpResponseRedirect(reverse('apldistro:store_detail'))

        self.data_context = {'form': form, 'store': store}
        return render(request, self.template, self.data_context)


class BrandList(View):
    template = 'apldistro/brand/brand_list.html'
    data_context = {}

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BrandList, self).dispatch(*args, **kwargs)

    def get(self, request):
        brands = Brand.objects.filter(status=True)
        self.data_context = {'brands': brands}
        return render(request, self.template, self.data_context)


class BrandAdd(View):
    form_brand_add = FormBrandAdd
    template = 'apldistro/brand/brand_add.html'
    data_context = {}

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BrandAdd, self).dispatch(*args, **kwargs)

    def get(self, request):
        form = self.form_brand_add()
        self.data_context['form'] = form
        return render(request, self.template, self.data_context)

    def post(self, request):
        form = self.form_brand_add(request.POST)

        if form.is_valid():
            brand = form.save(commit=False)
            brand.code = helper_generate_code()
            brand.status = True
            brand.save()
            messages.success(request, 'Brand successfully added')
            return HttpResponseRedirect(reverse('apldistro:brand_list'))

        self.data_context['form'] = form
        return render(request, self.template, self.data_context)


class BrandChange(View):
    form_brand_change = FormBrandChange
    template = 'apldistro/brand/brand_change.html'
    data_context = {}

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BrandChange, self).dispatch(*args, **kwargs)

    def get(self, request, brand_pk):
        brand = get_object_or_404(Brand, pk=brand_pk)
        form = self.form_brand_change(instance=brand)
        self.data_context['brand'] = brand
        self.data_context['form'] = form
        return render(request, self.template, self.data_context)

    def post(self, request, brand_pk):
        brand = get_object_or_404(Brand, pk=brand_pk)
        form = self.form_brand_change(instance=brand, data=request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand successfully changed.')
            return HttpResponseRedirect(reverse('apldistro:brand_list'))

        self.data_context['brand'] = brand
        self.data_context['form'] = form
        return render(request, self.template, self.data_context)


class BrandRemove(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BrandRemove, self).dispatch(*args, **kwargs)

    def get(self, request, brand_pk):
        brand = get_object_or_404(Brand, pk=brand_pk)
        
        if brand.article_set.exists():
            messages.warning(request, 'Brand cannot be deleted')
        else:
            brand.delete()
            messages.success(request, 'Brand successfully removed')

        return HttpResponseRedirect(reverse('apldistro:brand_list'))


class BrandConnect(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BrandConnect, self).dispatch(*args, **kwargs)

    def get(self, request, brand_pk):
        brand = get_object_or_404(Brand, pk=brand_pk)
        request.session['session_brand_pk'] = brand.pk
        request.session['session_brand_name'] = brand.name
        return HttpResponseRedirect(reverse('apldistro:brand_list'))

