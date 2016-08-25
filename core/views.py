# -*- encoding: utf-8 -*-
import csv
import json

import itertools
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, render_to_response, RequestContext, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from dv.helpers import Hangup
from ipdhcp.models import Dhcphosts_networks, Dhcphosts_hosts
from .auth_backend import AuthBackend
from .models import User, Payment, Fees, Dv, UserPi, Street, House, District, Dv_calls, Nas, ErrorsLog, Dv_log, Admin, num_to_ip, AdminSettings, \
    AdminLog, ip_to_num, Group
from ipdhcp.models import ipRange
from .forms import AdministratorForm, SearchForm, SearchFeesForm, SearchPaymentsForm, ClientForm
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .commands import strfdelta, sizeof_fmt
from django.contrib.auth.decorators import permission_required
from ws4redis.redis_store import RedisMessage, RedisStore
from ws4redis.publisher import RedisPublisher
import helpers
import platform
import psutil
import datetime
from django.core import serializers


def custom_redirect(url_name, *args, **kwargs):
    from django.core.urlresolvers import reverse
    import urllib
    url = reverse(url_name, args=args)
    params = urllib.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)


def get_pc_info(request):
    psutil.boot_time()
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    d2 = datetime.datetime.now()
    diff = abs((d2 - boot_time))
    if 'action' in request.GET and request.GET['action'] == 'get_pc_info':
        try:
            list = []
            data_dict = {}
            for getCpu in psutil.cpu_percent(interval=1, percpu=True):
                pinfo = {}
                pinfo['core'] = getCpu
                list.append(pinfo)
            data_dict.update({
                "cpu": list,
                "memory": [{
                    "cur": psutil.virtual_memory().percent,
                    "total": psutil.virtual_memory().total,
                    "used": psutil.virtual_memory().used,
                    "free": psutil.virtual_memory().free,
                    "cached": psutil.virtual_memory().cached,
                    "swap": psutil.swap_memory().percent,
                    "stotal": psutil.swap_memory().total,
                    "sused": psutil.swap_memory().used,
                    "sfree": psutil.swap_memory().free,
                }],
                "uptime": strfdelta(diff, settings.UPTIME_FORMAT)
            })

            get_pc_info = json.dumps(data_dict)
            cpus_info = RedisMessage('%s' % get_pc_info)  # create a welcome message to be sent to everybody
            RedisPublisher(facility=request.GET['room'], broadcast=True).publish_message(cpus_info)
        except Exception:
            pass
    return HttpResponse('Ok')


@login_required()
def index(request, settings=settings):
    ip_list_r = []
    ip_list_db = []
    sys = platform.platform()
    if 'pay_now' in request.GET:
        payments_now = Payment.objects.filter(date__icontains=datetime.datetime.now().date()).last()
        if payments_now != None:
            pay_list = {}
            pay_list['pay_now'] = payments_now.sum, payments_now.dsc, payments_now.uid.login, str(payments_now.uid.id), payments_now.aid.login
            res_json = json.dumps(pay_list)
            return HttpResponse(res_json)
    if 'pay' in request.GET:
        pay_list = {}
        result_day_pay = 0
        result_week_pay = 0
        payments_today = Payment.objects.filter(date__icontains=datetime.datetime.now().date())
        payments_week = Payment.objects.filter(date__lte=datetime.datetime.now().date() + datetime.timedelta(days=1), date__gte=(datetime.datetime.now().date() + datetime.timedelta(days=1)) - datetime.timedelta(weeks=1))
        payments_month = Payment.objects.filter(date__year=datetime.datetime.now().year, date__month=datetime.datetime.now().month)
        pay_list['pay_day'] = payments_today.aggregate(Sum('sum')), payments_today.count()
        pay_list['pay_week'] = payments_week.aggregate(Sum('sum')), payments_week.count()
        pay_list['pay_month'] = payments_month.aggregate(Sum('sum')), payments_month.count()
        res_json = json.dumps(pay_list)
        return HttpResponse(res_json)
    cpu_load_list = psutil.cpu_percent(interval=1, percpu=True)
    root_disk_usage = psutil.disk_usage('/')
    if 'process' in request.GET:
        try:
            list = []
            for proc in psutil.process_iter():
                pinfo = {}
                pinfo['pid'] = proc.pid
                pinfo['name'] = proc.name()
                pinfo['status'] = proc.status()
                pinfo['cpu'] = proc.cpu_percent().real
                list.append(pinfo)
            res_json = json.dumps(list)
            return HttpResponse(res_json)
        except Exception:
            pass
    if helpers.module_check('claims'):
        from claims.models import Claims, Queue
        queue = Queue.objects.all()
        claims_list_opened = Claims.objects.filter(state=1).count()
        claims_list_closed = Claims.objects.filter(state=2).count()
        list = []
        list1 = []
        for q in queue:
            list.append({'name': q.name, 'opened': q.claims.filter(state=1).count(), 'closed': q.claims.filter(state=2).count(), 'all': q.claims.all().count()})
        list1.append({'all_opened': claims_list_opened, 'all_closed': claims_list_closed})
    return render(request, 'index.html', locals())

@login_required()
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

@login_required()
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

@login_required()
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


@login_required()
# @permission_required('users.can_vote')
def search(request):

    all_table_choices = [
        'user_id__id',
        'user_id__login',
        'fio',
        'user_id__bill__deposit',
        'district',
        'street',
        'location',
        'kv',
        'user_id__credit',
        'user_id__disabled',
        'user_id__deleted',
    ]
    default_table_choices = [
        'user_id__login',
        'fio',
        'user_id__bill__deposit',
        'user_id__credit',
        'user_id__disabled',
        'user_id__deleted',
    ]
    search_form = SearchForm()
    search_fees_form = SearchFeesForm()
    search_payments_form = SearchPaymentsForm()
    districts = District.objects.all()
    filter_params = {}
    includes = []
    try:
        admin_settings = AdminSettings.objects.get(admin_id=request.user.id, object='USERS_LIST')
        default_table_choices = admin_settings.setting.lower().replace(' ', '').split(',')
    except AdminSettings.DoesNotExist:
        admin_settings = AdminSettings.objects.create(
            admin_id=request.user.id,
            object='USERS_LIST',
            setting=', '.join(default_table_choices)
        )

    if request.method == 'POST':
        includes = [', '.join(request.POST.getlist('includes'))]
        if any('user_id__login' in s for s in includes):
            pass
        else:
            includes.append('user_id__login')
        if any('user_id__deleted' in s for s in includes):
            pass
        else:
            includes.append('user_id__deleted')
        admin_settings.setting = ', '.join(includes)
        admin_settings.admin_id = request.user.id
        # admin_settings.save()
        return redirect(request.get_full_path())
    try:
        search = request.GET.get('search')
    except:
        search = None
    search_type = request.GET.get('search_type', '1')
    if search_type == '1':
        print request.GET
        search_form = SearchForm(request.GET, initial=request.GET)
        if request.GET.get('search'):
            order_by = request.GET.get('order_by', 'user_id__login')
            if 'uid' in request.GET and request.GET['uid'] != '':
                try:
                    user = User.objects.get(id=request.GET['uid'])
                    return redirect('core:client', uid=user.id)
                except User.DoesNotExist:
                    error = 'User not found'
                    return render(request, 'search.html', locals())
            else:
                if 'login' in request.GET and request.GET['login'] != '':
                    filter_params.update({'user_id__login__contains': request.GET['login']})
                if 'district' in request.GET and request.GET['district'] != '':
                    city = District.objects.get(id=request.GET['district'])
                    if 'street' not in request.GET or request.GET['street'] == '':
                        city_street = Street.objects.values('id').filter(district_id=request.GET['district'])
                        filter_params['street_id__in'] = city_street
                    else:
                        street = Street.objects.values_list('id').get(id=request.GET['street'])
                        filter_params.update({'street_id': street})
                        if 'house' in request.GET and request.GET['house'] != '':
                            house = House.objects.values_list('id').get(id=request.GET['house'])
                            filter_params.update({'location_id': house})
                if 'flat' in request.GET and request.GET['flat'] != '':
                    filter_params.update({'kv': request.GET['flat']})
                if 'disabled' in request.GET and request.GET['disabled'] != '':
                    filter_params.update({'user_id__disabled': 1})
                try:
                    print filter_params
                    print 'try'
                    userpi = UserPi.objects.filter(**filter_params).order_by(order_by)
                    if userpi.count() == 0:
                        error = 'User not found'
                    elif userpi.count() == 1:
                        for u in userpi:
                            return redirect('core:client', uid=u.user_id.id)
                    else:
                        print 'else'
                        all = userpi.count()
                        disabled = userpi.filter(user_id__disabled=1).count()
                        not_active = userpi.filter(user_id__disabled=2).count()
                        deleted = userpi.filter(user_id__deleted=1).count()
                        paginator = Paginator(userpi, 100)
                        page = request.GET.get('page', 1)
                        print '1'
                        try:
                            users = paginator.page(page)
                        except PageNotAnInteger:
                            users = paginator.page(1)
                        except EmptyPage:
                            users = paginator.page(paginator.num_pages)
                        if int(page) > 5:
                            start = str(int(page)-5)
                        else:
                            start = 1
                        print '2'
                        if int(page) < paginator.num_pages-5:
                            end = str(int(page)+5+1)
                        else:
                            end = paginator.num_pages+1
                        page_range = range(int(start), int(end)),
                        for p in page_range:
                            page_list = p
                        pre_end = users.paginator.num_pages - 2
                        print pre_end
                        print locals()
                    return render(request, 'search.html', locals())
                except User.DoesNotExist:
                    error = 'User not found'
                    return render(request, 'search.html', locals())
    elif search_type == '2':
        print 'company search'
    elif search_type == '3':
        search_fees_form = SearchFeesForm(request.GET, initial=request.GET)
        if request.GET.get('search'):
            order_by = request.GET.get('order_by', 'uid__login')
            if 'login' in request.GET and request.GET['login'] != '':
                filter_params.update({'uid__login__contains': request.GET['login']})
            if 'group' in request.GET and request.GET['group'] != '':
                filter_params.update({'uid__gid__id': request.GET['group']})
            print filter_params
            try:
                fees_list = Fees.objects.filter(**filter_params).order_by(order_by)
                if fees_list.count() == 0:
                    error = 'Fees not found'
                # elif userpi.count() == 1:
                #     for u in userpi:
                #         return redirect('core:client', uid=u['user_id'])
                else:
                    all = fees_list.count()
                    disabled = fees_list.filter(uid__disabled=1).count()
                    not_active = fees_list.filter(uid__disabled=2).count()
                    deleted = fees_list.filter(uid__deleted=1).count()
                    paginator = Paginator(fees_list, settings.FEES_PER_PAGE)
                    page = request.GET.get('page', 1)
                    try:
                        fees = paginator.page(page)
                    except PageNotAnInteger:
                        fees = paginator.page(1)
                    except EmptyPage:
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
                return render(request, 'search.html', locals())
            except Fees.DoesNotExist:
                error = 'User not found'
                return render(request, 'search.html', locals())
    elif search_type == '4':
        search_payments_form = SearchPaymentsForm(request.GET, initial=request.GET)
        order_by = request.GET.get('order_by', 'uid__login')
        if 'login' in request.GET and request.GET['login'] != '':
            filter_params.update({'uid__login__contains': request.GET['login']})
        if 'group' in request.GET and request.GET['group'] != '':
            filter_params.update({'uid__gid__id': request.GET['group']})
        try:
            payments_list = Payment.objects.filter(**filter_params).order_by(order_by)
            if payments_list.count() == 0:
                error = 'Payments not found'
            # elif userpi.count() == 1:
            #     for u in userpi:
            #         return redirect('core:client', uid=u['user_id'])
            else:
                all = payments_list.count()
                disabled = payments_list.filter(uid__disabled=1).count()
                not_active = payments_list.filter(uid__disabled=2).count()
                deleted = payments_list.filter(uid__deleted=1).count()
                paginator = Paginator(payments_list, settings.PAYMENTS_PER_PAGE)
                page = request.GET.get('page', 1)
                try:
                    payments = paginator.page(page)
                except PageNotAnInteger:
                    payments = paginator.page(1)
                except EmptyPage:
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
            return render(request, 'search.html', locals())
        except Payment.DoesNotExist:
            error = 'Payments not found'
            return render(request, 'search.html', locals())
    if 'global_search' in request.GET:
        global_list = {}
        userpi = UserPi.objects.all()
        userpi.filter(fio=request.GET['global_search'])
        print userpi.fio
        print 'global'
        print locals()
    return render(request, 'search.html', locals())


@login_required()
def client(request, uid):
    if 'hangup' in request.GET:
        hangup = Hangup(request.GET['nas_id'], request.GET['port_id'], request.GET['acct_session_id'], request.GET['user_name'])
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
            res = '<option value=' + str(item.id) + '>' + item.number.encode('utf8') + '</option>'
            dict_resp.append(res1 + res)
        return HttpResponse(dict_resp)
    try:
        client = User.objects.get(id=uid)
    except User.DoesNotExist:
        return render(request, '404.html', locals())
    client_form = ClientForm(instance=client)
    print client_form
    streets = Street.objects.all()
    houses = House.objects.all()
    group = Group.objects.all()
    dv_session = Dv_calls.objects.filter(uid=uid)
    if helpers.module_check('olltv'):
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
                        check_bundle = oll_check_bundle(account=client.id, tp=tp['sub_id'], hash=auth['hash'])
                        if check_bundle['mess'] == 'Error':
                            messages.warning(request, check_bundle)
                        else:
                            get_bundle_status = check_bundle['data']
                            tp.update({'status': get_bundle_status})
                            tp_list.append(tp)
        except Iptv.DoesNotExist:
            olltv_exist = False
    if 'show_password' in request.GET:
        user_password = client.get_hash_password
    else:
        user_password = ''
    dv = Dv.objects.get(user=uid)
    if helpers.module_check('claims'):
        from claims.models import Claims
        claims = Claims.objects.filter(uid=uid, state=1)
    return render(request, 'user_edit.html', locals())


def clients(request):
    filter_by = request.GET.get('users_status', '0')
    order_by = request.GET.get('order_by', 'login')
    users_list = User.objects.all().order_by(order_by)
    if filter_by == '1':
        users_list = users_list.filter(bill__deposit__gte=0, disabled=False, deleted=False,)
    if filter_by == '2':
        users_list = users_list.filter(bill__deposit__lt=0, credit=0)
    if filter_by == '3':
        users_list = users_list.filter(disabled=True, deleted=False)
    if filter_by == '4':
        users_list = users_list.filter(deleted=True)
    if filter_by == '5':
        users_list = users_list.filter(credit__gt=0)
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
    if 'xml' in request.GET:
        xml_data = serializers.serialize("xml", users)
        return render(request, 'base.xml', {'data': xml_data}, content_type="text/xml")
    if 'csv' in request.GET:
        return helpers.export_to_csv(request, users, fields=('id', 'login'), name='login')
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


@login_required()
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
    dv_session = Dv_calls.objects.filter(uid=uid)
    out_sum = 0
    order_by = request.GET.get('order_by', '-date')
    try:
        client = User.objects.get(id=uid)
    except User.DoesNotExist:
        return render(request, '404.html', locals())
    payments_list = Payment.objects.filter(uid=client.id).order_by(order_by)
    for ex_payments in payments_list:
        out_sum = out_sum + ex_payments.sum
    paginator = Paginator(payments_list, settings.PAYMENTS_PER_PAGE)
    page = request.GET.get('page', 1)
    if helpers.module_check('olltv'):
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
        del_payment = Payment.objects.get(id=request.GET['del'])
        print request.GET
        log = AdminLog(
            actions='test',
            datetime=datetime.datetime.now(),
            ip=ip_to_num('127.0.0.1'),
            user_id=uid,
            admin_id=40,
        )
        #log.save()
        #print log.admin
        #del_payment.delete()
    if 'xml' in request.GET:
        xml_data = serializers.serialize("xml", payments)
        return render(request, 'base.xml', {'data': xml_data}, content_type="text/xml")
    if 'csv' in request.GET:
        return helpers.export_to_csv(request, payments, fields=('id', 'uid'), name='login')
    return render(request, 'user_payments.html', locals())


def client_fees(request, uid):
    dv_session = Dv_calls.objects.filter(uid=uid)
    out_sum = 0
    order_by = request.GET.get('order_by', '-date')
    try:
        client = User.objects.get(id=uid)
    except User.DoesNotExist:
        return render(request, '404.html', locals())
    fees_list = Fees.objects.filter(uid=client.id).order_by(order_by)
    for ex_fees in fees_list:
        out_sum = out_sum + ex_fees.sum
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
    if 'export_submit' in request.POST:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
        writer = csv.writer(response)
        writer.writerow(['Service', 'Sum'])
        for ex_fees in fees_list.filter(uid=uid, date__range=(request.POST['Last'], request.POST['First'])):
            writer.writerow([ex_fees.dsc.encode('utf-8'), ex_fees.sum])
            out_sum = out_sum + ex_fees.sum
        writer.writerow(['', out_sum])
        return response
    if 'xml' in request.GET:
        xml_data = serializers.serialize("xml", fees)
        return render(request, 'base.xml', {'data': xml_data}, content_type="text/xml")
    if 'csv' in request.GET:
        return helpers.export_to_csv(request, fees, fields=('id', 'uid'), name='login')
    return render(request, 'user_fees.html', locals())


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
                message = RedisMessage('<span style="color: blue; opacity: 0.5;">%s: %s is logged in</span>' % (datetime.datetime.now().strftime("%H:%M:%S"), username))  # create a welcome message to be sent to everybody
                RedisPublisher(facility='global_chat', broadcast=True).publish_message(message)
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
    message = RedisMessage('<span style="color: red; opacity: 0.5;">%s: %s is logged out</span>' % (datetime.datetime.now().strftime("%H:%M:%S"), request.user.login))  # create a welcome message to be sent to everybody
    RedisPublisher(facility='global_chat', broadcast=True).publish_message(message)
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
    admin_form = AdministratorForm()
    if request.method == 'POST':
        if 'admin_remove' in request.POST:
            print 'admin_remove'
            print request.POST
            admin = Admin.objects.get(id=request.POST['uid'])
            admin.delete()
        elif 'admin_add' in request.POST:
            print 'admin_add'
            print request.POST
            admin_form = AdministratorForm(request.POST)
            if admin_form.is_valid():
                print 'valid'
                admin_form.save()
    return render(request, 'administrators.html', locals())


@login_required()
def administrator_edit(request, uid):
    try:
        admin = Admin.objects.get(pk=uid)
    except Admin.DoesNotExist:
        return render(request, '404.html', locals())
    else:
        admin_form = AdministratorForm(instance=admin)
        if request.method == 'POST':
            admin_form = AdministratorForm(request.POST, instance=admin)
            if admin_form.is_valid():
                admin_form.save()
                return redirect('core:administrators')
        return render(request, 'admin_edit.html', locals())


def test(request, template=".html"):
    """
    Show a room.
    """
    # context = {"room": get_object_or_404(ChatRoom, slug=slug)}
    return render(request, template, locals())


@csrf_exempt
def chat(request):
    admins = helpers.get_online()
    if request.method == 'POST' and request.POST != '':
        print request.POST
        if request.POST['message']:
            message = RedisMessage('<span style="">%s(%s): %s</span>' % (request.user.login, datetime.datetime.now().strftime("%H:%M:%S"), request.POST['message']))  # create a welcome message to be sent to everybody
            RedisPublisher(facility=request.POST['room'], broadcast=True).publish_message(message)
        else:
            print 'no message'
    return render(request, 'chat.html', locals())
