from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from .models import ArticleDetail, Article
from aplhelper.helpers import helper_session_brand_pk
from apldistro.models import Brand
from common.decorators import connecting_brand_required


@connecting_brand_required
def articledetail_list_popup(request):
    brand = helper_session_brand_pk(request)
    articledetails = ArticleDetail.objects.filter(article__keep=False, brand=brand)

    query = ''
    if 'query' in request.GET:
        query = request.GET.get('query')
        articledetails = articledetails.filter(
        article__keep=False,
        # size__name__contains=query,
        article__name__icontains=query,
        brand=brand)

    paginator = Paginator(articledetails, 10)
    page = request.GET.get('page')

    try:
        articledetails = paginator.page(page)
    except PageNotAnInteger:
        articledetails = paginator.page(1)
    except EmptyPage:
        articledetails = paginator.page(paginator.num_pages)


    data_context = {
        'articledetails': articledetails, 
        'brand': brand,
        'query': query}

    return render(request, 'aplinventory/articledetail/popup/articledetail_list_popup.html', data_context)