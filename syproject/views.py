#-*- coding: utf-8
from django.contrib import auth

from django.http import HttpResponseRedirect

from django.shortcuts import render, render_to_response

from django.views.decorators.csrf import csrf_protect, csrf_exempt

from django.template import RequestContext

@csrf_exempt
def login(request):

    username = request.POST.get('user', '')
    password = request.POST.get('pass', '')

    user = auth.authenticate(username=username, password=password)

    print "({3}) user/{0}, pass/{1}, object/{2}".format(username, password, user, login.__name__)

    if request.user.is_authenticated():
        if username == "admin":
            return HttpResponseRedirect('/admin/')
        return HttpResponseRedirect('/eforms/')

    if user is not None and user.is_active:
        auth.login(request, user)

        if username == "admin":
            return HttpResponseRedirect('/admin/')
        return HttpResponseRedirect('/eforms/')
    else:
        return render(request, 'login.html', locals())
        #return render_to_response('login.html', context_instance=RequestContext(request,locals()))



def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login/')
