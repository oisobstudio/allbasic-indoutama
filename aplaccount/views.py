from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import FormAccountLogin


def account_login(request):
    if request.method == 'POST':
        form = FormAccountLogin(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])

            # Jika user ada
            if user is not None:
                # Jika user aktif
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('aplbase:dashboard'))

                else:
                    # Jika user tidak aktif / diblokir
                    messages.error(request, 'Status anda diblokir.')

            else:
                # Jika user tidak ada/belum terdaftar
                messages.error(request, 'Anda belum terdaftar di dalam sistem ini.')
        else:
            # Jika form tidak valid.
            messages.error(request, 'Username and password not valid !')
    else:
        form = FormAccountLogin()
    data_context = {'form': form}
    return render(request, 'aplaccount/account_login.html', data_context)


def account_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('aplaccount:account_login'))