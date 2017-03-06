from uuid import uuid4
# from django.shortcuts import get_object_or_404
# from apldistro.models import Brand


def helper_generate_code():
    u = uuid4()
    gen = str(u)
    gen = gen.split('-')
    return gen[-1][:5].upper()


def helper_session_brand_pk(request):
    brand = get_object_or_404(Brand, pk=request.session['session_brand_pk'])
    return brand

