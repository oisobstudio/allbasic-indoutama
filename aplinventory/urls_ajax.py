from django.conf.urls import url
from . import view_ajax


urlpatterns = [
    url(r'^jax/articledetail/(?P<pk>[0-9]+)/(?P<stock>[0-9]+)/change/$',
        view_ajax.ajax_articledetail_change, name="ajax_articledetail_change"),
]