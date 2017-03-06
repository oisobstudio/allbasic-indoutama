from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import ArticleDetail


@login_required
@require_POST
def ajax_articledetail_change(request, pk, stock):
    try:
        articledetail = ArticleDetail.objects.get(pk=pk)
        articledetail.stock = stock
        articledetail.user = request.user
        articledetail.save()

        return JsonResponse({'status': True})
    except:
        return JsonResponse({'status': False})