# -*- encoding: utf-8 -*-
import random
import socket
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, render_to_response, RequestContext, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import pyrad
import sys
from dv.hangup import Hangup
from pyrad.client import Client, packet
from pyrad import server
from pyrad.dictionary import Dictionary
from .auth_backend import AuthBackend
from .models import User, Payment, Bill, Fees, Tp, ip_to_num, AdminLog, AbonTarifs, AbonUserList, Dv, num_to_ip, UserPi, Street, House, District, Dv_calls, Nas, ErrorsLog, Dv_log, Admin
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .commands import strfdelta, sizeof_fmt
import module_check
import platform
import psutil
import datetime
from django.http import JsonResponse



def custom_redirect(url_name, *args, **kwargs):
    from django.core.urlresolvers import reverse
    import urllib
    url = reverse(url_name, args=args)
    params = urllib.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)


@login_required()
def index(request, settings=settings):
    print request.POST
    if request.method == 'GET':
        print request.GET
    sys = platform.platform()
    psutil.boot_time()
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    d2 = datetime.datetime.now()
    diff = abs((d2 - boot_time))
    uptime = strfdelta(diff, settings.UPTIME_FORMAT)
    cpu_count = psutil.cpu_count()
    cpu_load_list = psutil.cpu_percent(interval=1, percpu=True)
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disks = psutil.disk_partitions()
    root_disk_usage = psutil.disk_usage('/')
    return render(request, 'index.html', locals())


def nas(request):
    if 'sessions' in request.GET:
        sessions = request.GET['sessions']
        session_list = Dv_calls.objects.filter(nas=request.GET['sessions'])
        all = session_list.count()
        guest = session_list.filter(guest=1).count()
        paginator = Paginator(session_list, 20)
        page = request.GET.get('page', 1)
        try:
            sespage = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            sespage = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            sespage = paginator.page(paginator.num_pages)
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
        pre_end = sespage.paginator.num_pages - 2
    nas_id = Nas.objects.all()
    return render(request, 'nas.html', locals())


def client_errors(request, uid):
    user = User.objects.get(id=uid)
    user_errors = ErrorsLog.objects.filter(user=user.login)
    paginator = Paginator(user_errors, settings.USER_ERRORS_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        errors = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        errors = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        errors = paginator.page(paginator.num_pages)
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
    pre_end = errors.paginator.num_pages - 2
    return render(request, 'user_errors.html', locals())


def client_statistics(request, uid):
    order_by = request.GET.get('order_by', '-start')
    user = User.objects.get(id=uid)
    user_statistics = Dv_log.objects.filter(uid=uid).order_by(order_by)
    paginator = Paginator(user_statistics, settings.USER_ERRORS_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        statistics = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        statistics = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        statistics = paginator.page(paginator.num_pages)
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
    pre_end = statistics.paginator.num_pages - 2
    return render(request, 'user_statistics.html', locals())


def search(request):
    user_list = None
    print request.POST
    if 'address' in request.POST:
        try:
            city = District.objects.get(id=request.POST['ADDRESS_DISTRICT'])
            userpi = UserPi.objects.filter(city=city, street__id__icontains=request.POST['ADDRESS_STREET'], location__id__icontains=request.POST['ADDRESS_BUILD'], kv__icontains=request.POST['flat']).order_by('id')
            if userpi.count() == 0:
                error = 'User not found'
            elif userpi.count() == 1:
                print 'asd'
                for u in userpi:
                    return redirect('core:client', uid=u.id_id)
            else:
                address = request.POST['address']
                all = userpi.count()
                paginator = Paginator(userpi, 20)
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
        except User.DoesNotExist:
            error = 'User not found'
            return render(request, 'search.html', locals())


    if 'uid' in request.POST and request.POST['uid'] != '':
        try:
            user = User.objects.get(id=request.POST['uid'])
            return redirect('core:client', uid=user.id)
        except User.DoesNotExist:
            error = 'User not found'
            return render(request, 'search.html', locals())
    if 'login' in request.POST and request.POST['login'] != '':
        login = request.POST['login']
        user_list = User.objects.filter(login__icontains=request.POST['login']).order_by('id')
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
    res1 = '<option selected="selected"></option>'
    if 'district' in request.GET:
        district = District.objects.all()
        dict_resp= []
        for item  in district:
            res = '<option value=' + str(item.id) + '>' + item.name + '</option>'
            dict_resp.append(res1 + res)
        return HttpResponse(dict_resp)

    if 'DISTRICT' in request.GET:
        street = Street.objects.filter(district_id=request.GET['DISTRICT'])
        dict_resp= []
        for item  in street:
            res = '<option value=' + str(item.id) + '>' + item.name + '</option>'
            dict_resp.append(res1 + res)
        return HttpResponse(dict_resp)

    if 'STREET' in request.GET:
        house = House.objects.filter(street_id=request.GET['STREET'])
        dict_resp= []
        for item in house:
            res = '<option value=' + str(item.id) + '>' + item.number.encode('utf8') + '</option>'
            dict_resp.append(res1 + res)
        return HttpResponse(dict_resp)
    return render(request, 'search.html', locals())


@login_required()
def client(request, uid):
    print request.GET
    if 'hangup' in request.GET:
        hangup = Hangup(request.GET['nas_id'], request.GET['acct_session_id'])

    res1 = '<option selected="selected"></option>'
    if 'district' in request.GET:
        district = District.objects.all()
        dict_resp= []
        for item  in district:
            res = '<option value=' + str(item.id) + '>' + item.name + '</option>'
            dict_resp.append(res1 + res)
        return HttpResponse(dict_resp)

    if 'DISTRICT' in request.GET:
        street = Street.objects.filter(district_id=request.GET['DISTRICT'])
        dict_resp = []
        for item in street:
            res = '<option value=' + str(item.id) + '>' + item.name + '</option>'
            dict_resp.append(res1 + res)
        return HttpResponse(dict_resp)

    if 'STREET' in request.GET:
        house = House.objects.filter(street_id=request.GET['STREET'])
        dict_resp= []
        for item in house:
            res = '<option value=' + str(item.street_id) + '>' + item.number.encode('utf8') + '</option>'
            dict_resp.append(res1 + res)
        return HttpResponse(dict_resp)
    user = User.objects.get(id=uid)
    #bill = Bill.objects.get(company_id=user.company)
    #print bill
    streets = Street.objects.all()
    houses = House.objects.all()
    dv_session = Dv_calls.objects.filter(uid=uid)
    if module_check.check('olltv'):
        from olltv.models import Iptv, IptvDevice, IptvDeviceType
        from olltv.api import oll_user_info, oll_check_bundle, olltv_auth
        try:
            user_olltv = Iptv.objects.get(uid=uid)
            olltv_exist = True
            user_olltv_dev = IptvDevice.objects.filter(uid=uid)
            try:
                auth = olltv_auth()
            except:
                auth = None
            if auth != None:
                user_info = oll_user_info(account=uid, hash=auth['hash'])
                get_user_info = user_info['data']
                tp_list_dict = user_info['data']['bought_subs']
                tp_count = user_info['tp_count']
                tp_list = []
                if tp_count < 1:
                    tp_list = None
                else:
                    for tp in tp_list_dict:
                        # check_bundle
                        check_bundle = oll_check_bundle(account=user.id, tp=tp['sub_id'], hash=auth['hash'])
                        if check_bundle['mess'] == 'Error':
                            messages.warning(request, check_bundle)
                        else:
                            get_bundle_status = check_bundle['data']
                            tp.update({'status': get_bundle_status})
                            tp_list.append(tp)
        except Iptv.DoesNotExist:
            olltv_exist = False
    if 'show_password' in request.GET:
        user_password = user.get_hash_password
    else:
        user_password = ''
    dv = Dv.objects.get(user=uid)
    # if 'dv_submit' in request.POST:
    #     print 'yes'
    # else:
    #     print 'no'
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
    if module_check.check('olltv'):
        olltv_module = True
    else:
        olltv_module = False
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
        return render(request, 'layout_edit.html', locals())
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


@login_required()
def administrators(request):
    admins = Admin.objects.all()
    return render(request, 'administrators.html', locals())

