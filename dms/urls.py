from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import tornado.web


urlpatterns = [
    url(r'', include('aplaccount.urls', namespace='aplaccount')),
    url(r'^base/', include('aplbase.urls', namespace='aplbase')),
    url(r'^distro/', include('apldistro.urls', namespace='apldistro')),
    url(r'^inventory/', include('aplinventory.urls', namespace='aplinventory')),
    url(r'^transaction/', include('apltransaction.urls', namespace="apltransaction")),
    url(r'', include('aplaccount.urls', namespace='aplaccount')),
    url(r'^billship/', include('aplbillship.urls', namespace='aplbillship')),
    url(r'^report/', include('aplreport.urls', namespace='aplreport')),
    url(r'^promotion/', include('aplpromotion.urls', namespace='aplpromotion')),
    url(r'^admin/', include(admin.site.urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




