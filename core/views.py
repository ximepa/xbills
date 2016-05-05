# -*- encoding: utf-8 -*-
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, render_to_response, RequestContext, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .auth_backend import AuthBackend
from .models import User, Payment, Bill, Fees, Iptv, Tp, ip_to_num, AdminLog, AbonTarifs, AbonUserList, Dv, num_to_ip, UserPi
from django.contrib import messages
#from olltv.api import olltv_auth, olltv_users_list, oll_user_check, oll_user_add, oll_user_bind, oll_user_unbind, oll_user_info, oll_check_bundle, oll_get_device, oll_dev_check, oll_dev_add, oll_disable_bundle, oll_dev_remove, oll_add_bundle, olltv_change_email, olltv_change_userinfo, oll_account_check
#from olltv.forms import TypeForm, DeviceRemoveForm, DeviceAddForm
#from olltv.commands import make_conversion
#from olltv.models import IptvDeviceType, IptvDevice
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

modules = settings.INSTALLED_APPS

def custom_redirect(url_name, *args, **kwargs):
    from django.core.urlresolvers import reverse
    import urllib
    url = reverse(url_name, args=args)
    params = urllib.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)


@login_required()
def index(request):
    if 'index' in request.GET:
        index = request.GET.getlist('index')[0]
    else:
        return render(request, 'index.html', locals())
    return render(request, 'layout.html', locals())


def search(request):
    # search
    user_list = None
    if 'uid' in request.POST and request.POST['uid'] != '':
        try:
            user = User.objects.get(id=request.POST['uid'])
            return redirect('core:client', uid=user.id)
        except User.DoesNotExist:
            error = 'User not found'
            return render(request, 'search.html', locals())
    if 'login' in request.POST and request.POST['login'] != '':
        login = request.GET['login']
        user_list = User.objects.filter(login__icontains=request.GET['login']).order_by('id')
        if user_list.count() == 0:
            error = 'User not found'
        elif user_list.count() == 1:
            for u in user_list:
                return redirect('core:client', uid=u.id)
        else:
            all = user_list.count()
            end = user_list.filter(deleted=1).count()
            disabled = user_list.filter(disabled=1).count()
            deleted = user_list.filter(deleted=1).count()
            paginator = Paginator(user_list, 20)
            page = request.GET.get('page', 1)
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                users = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                users = paginator.page(paginator.num_pages)
            if int(page) > 5:
                start = str(int(page)-5)
            else:
                start = 1
            if int(page) < paginator.num_pages-5:
                end = str(int(page)+5+1)
            else:
                end = paginator.num_pages+1
            page_range = range(int(start), int(end)),
            for p in page_range:
                page_list = p
            pre_end = users.paginator.num_pages - 2
        return render(request, 'search.html', locals())
    return render(request, 'search.html', locals())


def client(request, uid):
    print request.POST
    if 'dv_submit' in request.POST:
        print 'yes'
    else:
        user = User.objects.get(id=uid)
        user_pi = UserPi.objects.get(id=uid)
        bill = Bill.objects.get(uid=uid)
        if 'show_password' in request.GET:
            user_password = user.get_hash_password
        dv = Dv.objects.get(user=uid)
        ip = num_to_ip(dv.ip)
        netmask = num_to_ip(dv.netmask)
    return render(request, 'user_edit.html', locals())


def clients(request):
    users_list = User.objects.all().order_by('login')
    all = users_list.count()
    end = users_list.filter(deleted=1).count()
    disabled = users_list.filter(disabled=1).count()
    deleted = users_list.filter(deleted=1).count()
    paginator = Paginator(users_list, 100)
    page = request.GET.get('page', 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)
    if int(page) > 5:
        start = str(int(page)-5)
    else:
        start = 1
    if int(page) < paginator.num_pages-5:
        end = str(int(page)+5+1)
    else:
        end = paginator.num_pages+1
    page_range = range(int(start), int(end)),
    for p in page_range:
        page_list = p
    pre_end = users.paginator.num_pages - 2
    return render(request, 'users.html', locals())



def payments(request):
    order_by = request.GET.get('order_by', '-date')
    payments_list = Payment.objects.all().order_by(order_by)
    paginator = Paginator(payments_list, settings.PAYMENTS_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        payments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        payments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        payments = paginator.page(paginator.num_pages)
    if int(page) > 5:
        start = str(int(page)-5)
    else:
        start = 1
    if int(page) < paginator.num_pages-5:
        end = str(int(page)+5+1)
    else:
        end = paginator.num_pages+1
    page_range = range(int(start), int(end)),
    for p in page_range:
        page_list = p
    pre_end = payments.paginator.num_pages - 2
    return render(request, 'payments.html', locals())


def fees(request):
    order_by = request.GET.get('order_by', '-date')
    fees_list = Fees.objects.all().order_by(order_by)
    paginator = Paginator(fees_list, settings.FEES_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        fees = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        fees = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        fees = paginator.page(paginator.num_pages)
    if int(page) > 5:
        start = str(int(page)-5)
    else:
        start = 1
    if int(page) < paginator.num_pages-5:
        end = str(int(page)+5+1)
    else:
        end = paginator.num_pages+1
    page_range = range(int(start), int(end)),
    for p in page_range:
        page_list = p
    pre_end = fees.paginator.num_pages - 2
    return render(request, 'fees.html', locals())


def client_payments(request, uid):
    order_by = request.GET.get('order_by', '-date')
    user = User.objects.get(id=uid)
    payments_list = Payment.objects.filter(uid=user.id).order_by(order_by)
    paginator = Paginator(payments_list, settings.PAYMENTS_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        payments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        payments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        payments = paginator.page(paginator.num_pages)
    if int(page) > 5:
        start = str(int(page)-5)
    else:
        start = 1
    if int(page) < paginator.num_pages-5:
        end = str(int(page)+5+1)
    else:
        end = paginator.num_pages+1
    page_range = range(int(start), int(end)),
    for p in page_range:
        page_list = p
    pre_end = payments.paginator.num_pages - 2
    if 'del' in request.GET:
        return redirect(request.GET['return_url'])
    return render(request, 'payments.html', locals())


def client_fees(request, uid):
    order_by = request.GET.get('order_by', '-date')
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        error = 'user not found'
        return render(request, 'layout.html', locals())
    fees_list = Fees.objects.filter(uid=user.id).order_by(order_by)
    paginator = Paginator(fees_list, settings.FEES_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        fees = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        fees = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        fees = paginator.page(paginator.num_pages)
    if int(page) > 5:
        start = str(int(page)-5)
    else:
        start = 1
    if int(page) < paginator.num_pages-5:
        end = str(int(page)+5+1)
    else:
        end = paginator.num_pages+1
    page_range = range(int(start), int(end)),
    for p in page_range:
        page_list = p
    pre_end = fees.paginator.num_pages - 2
    if 'del' in request.GET:
        return redirect(request.GET['return_url'])
    return render(request, 'fees.html', locals())


def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        print request.POST
        username = request.POST['username']
        password = request.POST['password']
        user = AuthBackend().authenticate(username=username, password=password)
        if user is None:
            error = u'Ім’я користувача або пароль введені невірно'
            return render(request, 'login.html', locals())
        elif user is not None:
            if user:
                user.backend = 'core.auth_backend.AuthBackend'
                login(request, user)
                return HttpResponseRedirect(request.GET['next'])
            else:
                error = u'Аккаунт заблоковано'
                return render(request, 'login.html', locals())
        else:
            # Bad login details were provided. So we can't log the user in.
            error = "Invalid login details: {0}, {1}".format(username, password)
            return render(request, 'login.html', locals())
    else:
        return render(request, 'login.html', locals())


@login_required()
def logout_view(request):
    logout(request)
    return redirect('core:index')


@login_required()
def user_group(request, uid):
    user = User.objects.get(id=uid)
    return render(request, 'user_payments.html', locals())


@login_required()
def user_company(request, uid):
    user = User.objects.get(id=uid)
    return render(request, 'user_payments.html', locals())