from django.conf.urls import url
from . import views
from . import views_popup
from . import urls_ajax

urlpatterns = [

    # SizeType URL
    url(r'^sizecategory\.html$', views.SizeCategoryList.as_view(), name='sizecategory_list'),
    url(r'^sizecategory/add\.html$', views.SizeCategoryAdd.as_view(), name='sizecategory_add'),
    url(r'^sizecategory/(?P<size_category_pk>[0-9]+)/change\.html$', views.SizeCategoryChange.as_view(), name='sizecategory_change'),
    url(r'^sizecategory/(?P<size_category_pk>[0-9]+)/remove\.html$', views.SizeCategoryRemove.as_view(), name='sizecategory_remove'),

    # # Size URL
    url(r'size\.html$', views.size_list, name='size_list'),
    url(r'size/(?P<pk_sizecategory>[0-9]+)/add\.html$', views.size_add, name='size_add'),
    url(r'size/(?P<pk_size>[0-9]+)/change\.html$', views.size_change, name='size_change'),
    url(r'size/(?P<pk_size>[0-9]+)/removed\.html$', views.size_remove, name='size_remove'),

    # Product Category URL
    url(r'^productcategory/$', views.productcategory_list, name='productcategory_list'),
    url(r'^productcategory/add/$', views.productcategory_add, name='productcategory_add'),
    url(r'^productcategory/(?P<pk_productcategory>[0-9]+)/change/$', views.productcategory_change, name='productcategory_change'),
    url(r'^productcategory/(?P<pk_productcategory>[0-9]+)/remove/$', views.productcategory_remove, name='productcategory_remove'),

    # Product URL
    url(r'^product/$', views.product_list, name='product_list'),
    url(r'^product/add/$', views.product_add, name='product_add'),
    url(r'^product/(?P<code_product>[\w\-]+)/change/$', views.product_change, name='product_change'),
    url(r'^product/(?P<code_product>[\w\-]+)/remove/$', views.product_remove, name='product_remove'),

    # Article URL
    url(r'^article/$', views.article_list, name='article_list'),
    url(r'^article/add/$', views.article_add, name='article_add'),
    url(r'^article/(?P<pk_article>[0-9]+)/change/$', views.article_change, name='article_change'),
    url(r'^article/(?P<pk_article>[0-9]+)/remove/$', views.article_remove, name='article_remove'),
    url(r'^article/(?P<pk_article>[0-9]+)/keep/$', views.article_keep, name='article_keep'),
    url(r'^article/(?P<code>[\w\-]+)/print/barcode.pdf/$', views.article_printbarcode, name='article_printbarcode'),
    
    # ArticleDetail URL
    url(r'^articledetail/(?P<pk_article>[0-9]+)/(?P<pk_sizecategory>[0-9]+)/add/$',
        views.articledetail_add, name='articledetail_add'),
    url(r'^articledetail/(?P<pk_article>[0-9]+)/(?P<pk_articledetail>[0-9]+)/change/$', 
        views.articledetail_change, name='articledetail_change'),
    url(r'^articledetail/(?P<code>[\w\-]+)/remove/$',
        views.articledetail_remove, name='articledetail_remove'),

    # ArticleDetail Popup URL
    url(r'^popup/articledetail/', views_popup.articledetail_list_popup, name='articledetail_list_popup'),

    #
    # # ArticleDetail POPUP URL
    # url(r'articledetail/popup/$', views.articledetail_list_popup, name='articledetail_list_popup'),
]