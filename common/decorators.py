from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect
from django.core.urlresolvers import reverse
from apltransaction.models import TransactionDetail, Invoice
from django.shortcuts import get_object_or_404
from django.contrib import messages


## -----------------------------------------------------------------------------------
##                  INVOICE STORE 
## -----------------------------------------------------------------------------------


def connecting_brand_required(f):
    def wrap(request, *args, **kwargs):
        if not request.session.get('session_brand_pk'):
            messages.error(request, 'You must connecting brand !')
            return HttpResponseRedirect(reverse('apldistro:brand_list'))
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap



