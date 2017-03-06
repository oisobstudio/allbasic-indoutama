# Python package import
from uuid import uuid4
# Django package import
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.db.models import Count
from django.db.models import Avg
from django.db.models import Q
from django.db import IntegrityError
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# This app import
from .models import SizeCategory
from .models import Size
from .models import ProductCategory
from .models import Product
from .models import Article
from .models import ArticleDetail
from .forms import FormSizeCategoryAdd
from .forms import FormSizeCategoryChange
from .forms import FormAddSize
from .forms import FormChangeSize
from .forms import FormAddProductCategory
from .forms import FormChangeProductCategory
from .forms import FormAddProduct
from .forms import FormChangeProduct
from .forms import FormAddArticle
from .forms import FormChangeArticle
from .forms import FormAddArticleDetail
from .forms import FormChangeArticleDetail
from .forms import FormSearchProduct
# aplhelper import
from aplhelper.helpers import helper_generate_code
from aplhelper.helpers import helper_session_brand_pk
# apldistro import
from apldistro.models import Brand
# common import
from common.decorators import connecting_brand_required

class SizeCategoryList(View):
    data_context = {}
    template = 'aplinventory/sizecategory/sizecategory_list.html'

    @method_decorator(login_required)
    @method_decorator(connecting_brand_required)
    def dispatch(self, *args, **kwargs):
        return super(SizeCategoryList, self).dispatch(*args, **kwargs)

    def get(self, request):
        sizecategories = SizeCategory.objects.all()
        self.data_context = {'sizecategories': sizecategories}
        return render(request, self.template, self.data_context)


class SizeCategoryAdd(View):
    form_size_category_add = FormSizeCategoryAdd
    data_context = {}
    template = 'aplinventory/sizecategory/sizecategory_add.html'

    @method_decorator(login_required)
    @method_decorator(connecting_brand_required)
    def dispatch(self, *args, **kwargs):
        return super(SizeCategoryAdd, self).dispatch(*args, **kwargs)

    def get(self, request):
        brand = helper_session_brand_pk(request)
        form = self.form_size_category_add()
        self.data_context['form'] = form
        return render(request, self.template, self.data_context)

    def post(self, request):
        brand = helper_session_brand_pk(request)
        form = self.form_size_category_add(request.POST)
        if form.is_valid():
            size_category = form.save(commit=False)
            size_category.user = request.user
            size_category.brand = brand
            size_category.status = True
            size_category.save()
            messages.success(request, 'Size Category successfully added')
            return HttpResponseRedirect(reverse('aplinventory:size_add', 
                                        kwargs={'pk_sizecategory': size_category.pk}))

        self.data_context['form'] = form
        return render(request, self.template, self.data_context)


class SizeCategoryChange(View):
    form_size_category_change = FormSizeCategoryChange
    data_context = {}
    template = 'aplinventory/sizecategory/sizecategory_change.html'

    @method_decorator(login_required)
    @method_decorator(connecting_brand_required)
    def dispatch(self, *args, **kwargs):
        return super(SizeCategoryChange, self).dispatch(*args, **kwargs)

    def get(self, request, size_category_pk):
        brand = helper_session_brand_pk(request)
        size_category = get_object_or_404(SizeCategory, pk=size_category_pk)
        form = self.form_size_category_change(instance=size_category)
        self.data_context['form'] = form
        self.data_context['size_category'] = size_category
        return render(request, self.template, self.data_context)

    def post(self, request, size_category_pk):
        brand = helper_session_brand_pk(request)
        size_category = get_object_or_404(SizeCategory, pk=size_category_pk)
        form = self.form_size_category_change(instance=size_category, data=request.POST)

        if form.is_valid():
            size_category = form.save(commit=False)
            size_category.user = request.user
            size_category.save()
            messages.success(request, 'Size Category successfully changed.')
            return HttpResponseRedirect(reverse('aplinventory:sizecategory_list'))

        self.data_context['size_category'] = size_category
        self.data_context['form'] = form
        return render(request, self.template, self.data_context)


class SizeCategoryRemove(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SizeCategoryRemove, self).dispatch(*args, **kwargs)

    def get(self, request, size_category_pk):
        size_category = get_object_or_404(SizeCategory, pk=size_category_pk)

        if size_category.size_set.exists():
            messages.error(request, 'Size Category cannot delete.')
        else:
            size_category.delete()
            messages.success(request, 'Size Category successfully removed.')

        return HttpResponseRedirect(reverse('aplinventory:sizecategory_list'))

class SizeList(View):
    data_context = {}
    template = 'aplinventory/size/size_list.html'

    @method_decorator(login_required)
    @method_decorator(connecting_brand_required)
    def dispatch(self, *args, **kwargs):
        return super(SizeList, self).dispatch(*args, **kwargs)

    


@connecting_brand_required
def size_list(request):
    brand = helper_session_brand_pk(request)
    sizes = Size.objects.all()
    data_context = {'sizes': sizes}
    return render(request, 'aplinventory/size/size_list.html', data_context)


@connecting_brand_required
def size_add(request, pk_sizecategory):
    brand = helper_session_brand_pk(request)
    sizecategory = get_object_or_404(SizeCategory, pk=pk_sizecategory)
    sizes = Size.objects.filter(size_category=sizecategory)
    if request.method == 'POST':
        form = FormAddSize(data=request.POST)
        if form.is_valid():
            size = form.save(commit=False)
            size.user = request.user
            size.brand = brand
            size.size_category = sizecategory

            # Handling size same. integrity error ...
            try:
                size.save()
                messages.success(request, 'Size successfully added')
            except IntegrityError:
                messages.warning(request, 'Size not be same !')

            return HttpResponseRedirect(reverse('aplinventory:size_add',
                                                kwargs={'pk_sizecategory': pk_sizecategory}))
    else:
        form = FormAddSize()

    data_context = {'form': form, 'sizecategory': sizecategory, 'sizes': sizes}
    return render(request, 'aplinventory/size/size_add.html', data_context)


@connecting_brand_required
def size_change(request, pk_size):
    size = get_object_or_404(Size, pk=pk_size)

    if request.method == 'POST':
        form = FormChangeSize(data=request.POST, instance=size)
        if form.is_valid():
            size_frm = form.save(commit=False)
            size_frm.user = request.user
            size_frm.save()
            messages.success(request, 'Size successfully changed')
            return HttpResponseRedirect(reverse('aplinventory:sizecategory_list'))
    else:
        form = FormChangeSize(instance=size)

    data_context = {'form': form, 'size': size}
    return render(request, 'aplinventory/size/size_change.html', data_context)


@connecting_brand_required
def size_remove(request, pk_size):
    size = get_object_or_404(Size, pk=pk_size)
    if size.articledetail_set.count() > 0:
        messages.error(request, 'Size Cannot delete or update a parent row: a foreign key constaint fails.')
    else:
        size.delete()
        messages.success(request, 'Size successfully removed')
    return HttpResponseRedirect(reverse('aplinventory:sizecategory_list'))


@connecting_brand_required
def productcategory_list(request):
    productcategories = ProductCategory.objects.all()
    data_context = {'productcategories': productcategories}
    return render(request, 'aplinventory/productcategory/productcategory_list.html', data_context)


@connecting_brand_required
def productcategory_add(request):
    brand = helper_session_brand_pk(request)
    if request.method == 'POST':
        form = FormAddProductCategory(brand, request.POST)
        if form.is_valid():
            productcategory = form.save(commit=False)
            productcategory.user = request.user
            productcategory.brand = brand
            productcategory.save()
            messages.success(request, 'Product category successfully added')
            return HttpResponseRedirect(reverse('aplinventory:productcategory_list'))
    else:
        form = FormAddProductCategory(brand)

    data_context = {'form': form}
    return render(request, 'aplinventory/productcategory/productcategory_add.html', data_context)


@connecting_brand_required
def productcategory_change(request, pk_productcategory):
    productcategory = get_object_or_404(ProductCategory,
                                        pk=pk_productcategory)

    brand = productcategory.brand

    if request.method == 'POST':
        form = FormChangeProductCategory(brand, data=request.POST,
                                         instance=productcategory)
        if form.is_valid():
            productcategory_frm = form.save(commit=False)
            productcategory_frm.user = request.user
            productcategory_frm.save()
            messages.success(request, 'Product category successfully changed')
            return HttpResponseRedirect(reverse('aplinventory:productcategory_list'))
    else:
        form = FormChangeProductCategory(brand, instance=productcategory)

    data_context = {'form': form,
                    'productcategory': productcategory}
    return render(request,
                  'aplinventory/productcategory/productcategory_change.html',
                  data_context)


@connecting_brand_required
def productcategory_remove(request, pk_productcategory):
    productcategory = get_object_or_404(ProductCategory,
                                        pk=pk_productcategory)

    if productcategory.product_set.count() > 0:
        messages.warning(request, 'This data can not be deleted because they have data that is associated with it')
    else:
        productcategory.delete()
        messages.success(request, 'Product category successfully removed')
    return HttpResponseRedirect(reverse('aplinventory:productcategory_list'))


@connecting_brand_required
def product_list(request):
    object_list = Product.objects.all()

    page = request.GET.get('page')
    query = ''

    if 'query' in request.GET:
        form = FormSearchProduct(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            query = cd['query']
            object_list = object_list.filter(name__icontains=cd['query'])
    else:
        form = FormSearchProduct()

    paginator = Paginator(object_list, 10) # 10 Page show in page
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)


    data_context = {'products': products, 'query': query, 'form': form} 
    return render(request, 'aplinventory/product/product_list.html', data_context)


@connecting_brand_required
def product_add(request):
    brand = helper_session_brand_pk(request)
    if request.method == 'POST':
        form = FormAddProduct(brand, data=request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.brand = brand
            product.code = helper_generate_code()
            product.save()
            messages.success(request, 'Product successfully added')
            return HttpResponseRedirect(reverse('aplinventory:product_list'))
    else:
        form = FormAddProduct(brand)
    data_context = {'form': form}
    return render(request, 'aplinventory/product/product_add.html', data_context)


def product_change(request, code_product):
    product = get_object_or_404(Product, code=code_product)
    brand = product.brand

    if request.method == 'POST':
        form = FormChangeProduct(brand, data=request.POST, instance=product)
        if form.is_valid():
            product_frm = form.save(commit=False)
            product_frm.user = request.user
            product_frm.save()
            messages.success(request, 'Product successfully changed')
            return HttpResponseRedirect(reverse('aplinventory:product_list'))
    else:
        form = FormChangeProduct(brand, instance=product)

    data_context = {'form': form, 'product': product}
    return render(request, 'aplinventory/product/product_change.html', data_context)


def product_remove(request, code_product):
    product = get_object_or_404(Product, code=code_product)
    if product.article_set.count() > 0:
        messages.warning(request, 'This data can not be deleted because they have data that is associated with it')
    else:
        product.delete()
        messages.success(request, 'Product successfully removed')
    return HttpResponseRedirect(reverse('aplinventory:product_list'))


def article_list(request):

    object_list = Article.objects.all()
    query = ""
    
    if 'query' in request.GET:
        query = request.GET.get('query')
        object_list = object_list.filter(name__contains=query)

    paginator = Paginator(object_list, 10) # 10 Page show in page
    page = request.GET.get('page')

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    data_context = {'articles': articles, 'query':query}
    return render(request, 'aplinventory/article/article_list.html', data_context)


@connecting_brand_required
def article_add(request):
    brand = helper_session_brand_pk(request)
    if request.method == 'POST':
        form = FormAddArticle(brand, data=request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            article.code = helper_generate_code()
            pk_sizecategory = article.product.product_category.sizecategory.pk
            article.user = request.user
            article.brand = brand
            article.save()
            messages.success(request, 'Article successfully added')
            data_context_redirect = {'pk_article':article.pk, 'pk_sizecategory':pk_sizecategory}
            return HttpResponseRedirect(reverse('aplinventory:articledetail_add', kwargs=data_context_redirect))
    else:
        form = FormAddArticle(brand)

    data_context = {'form': form}
    return render(request, 'aplinventory/article/article_add.html', data_context)


def article_change(request, pk_article):
    article = get_object_or_404(Article, pk=pk_article)
    if request.method == 'POST':
        form = FormChangeArticle(data=request.POST, instance=article)
        if form.is_valid():
            article_frm = form.save(commit=False)
            article_frm.user = request.user
            article_frm.keep = False
            article_frm.save()
            messages.success(request, 'Article successfully changed')
            return HttpResponseRedirect(reverse('aplinventory:article_list'))
    else:
        form = FormChangeArticle(instance=article)
    
    data_context = {'form': form, 'article': article}
    return render(request, 'aplinventory/article/article_change.html', data_context)


def article_remove(request, pk_article):
    article = get_object_or_404(Article, pk=pk_article)
    article.delete()
    messages.success(request, 'Article successfully removed')
    return HttpResponseRedirect(reverse('aplinventory:article_list'))


def article_keep(request, pk_article):
    article = get_object_or_404(Article, pk=pk_article)
    if article.keep:
        article.keep = False
    else:
        article.keep = True
    article.save()
    messages.success(request, 'Article successfully keeped')
    return HttpResponseRedirect(reverse('aplinventory:article_list'))


def article_printbarcode(request, code):
    # code -> article code
    article = get_object_or_404(Article, code=code)
    data_context = {'article': article}
    return render(request, 'aplinventory/article/article_printbarcode.html', data_context)


def articledetail_add(request, pk_article, pk_sizecategory):
    # mengambil objek 'article' dari brand__pk dan pk
    # brand = helper_session_brand_pk(request)
    article = get_object_or_404(Article,
                                pk=pk_article,
                                keep=False)

    brand = article.brand

    articledetails = ArticleDetail.objects.filter(article=article)
    sizecategory = get_object_or_404(SizeCategory, pk=pk_sizecategory)

    # mengambil object 'size' dari object sizetype
    sizes = sizecategory.size_set.filter(brand=brand)

    if request.method == 'POST':
        form = FormAddArticleDetail(sizes, data=request.POST)
        if form.is_valid():
            articledetail = form.save(commit=False)
            articledetail.user = request.user
            articledetail.article = article
            articledetail.brand = brand
            articledetail.code = helper_generate_code()
            try:
                articledetail.save()
                messages.success(request, 'Detail Article successfully added')
            except IntegrityError:
                messages.warning(request, 'must not be the same size in the article.')

            return HttpResponseRedirect(reverse('aplinventory:articledetail_add',
                                            kwargs={'pk_article':pk_article, 
                                            'pk_sizecategory': pk_sizecategory}))
    else:
        form = FormAddArticleDetail(sizes)

    return render(request, 'aplinventory/articledetail/articledetail_add.html',
                  {'form': form, 'article': article, 'articledetails': articledetails})


def articledetail_change(request, pk_article, pk_articledetail):
    article = get_object_or_404(Article, pk=pk_article)
    articledetail = get_object_or_404(ArticleDetail, 
                                      pk=pk_articledetail,
                                      article=article)
    pk_sizecategory = articledetail.article.product.product_category.sizecategory.pk

    brand = articledetail.brand
    sizecategory = articledetail.size.size_category
    
    if request.method == 'POST':
        form = FormChangeArticleDetail(brand, sizecategory, data=request.POST, instance=articledetail)
        if form.is_valid():
            articledetail_frm = form.save(commit=False)
            articledetail_frm.user = request.user
            try:
                articledetail_frm.save()
                messages.success(request, 'Article Detail successfully changed')
            except IntegrityError:
                messages.warning(request, 'must not be the same size in the article.')

            return HttpResponseRedirect(reverse('aplinventory:articledetail_add',
                                            kwargs={
                                                'pk_article':pk_article, 
                                                'pk_sizecategory': pk_sizecategory}))
    else:
        form = FormChangeArticleDetail(brand, sizecategory, instance=articledetail)
        
    data_context = {'form': form}
    return render(request, 'aplinventory/articledetail/articledetail_change.html', data_context)


def articledetail_remove(request, code):
    articledetail = get_object_or_404(ArticleDetail, code=code)
    pk_article = articledetail.article.pk
    pk_sizecategory = articledetail.article.product.product_category.sizecategory.pk
    articledetail.delete()
    messages.success(request, 'Article Detail successfully removed')
    return HttpResponseRedirect(reverse('aplinventory:articledetail_add',
                                            kwargs={
                                                'pk_article':pk_article, 
                                                'pk_sizecategory': pk_sizecategory}))
