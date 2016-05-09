# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from core.models import User, Tp, Iptv, Bill, Fees, Shedule, AdminLog, Admin, ip_to_num, UserPi, AbonTarifs, AbonUserList, TpGroups
from .forms import UserFilterForm, DeviceAddForm, TypeForm, DeviceRemoveForm, GroupFilterForm
from django.conf import settings
from .models import IptvDeviceType, IptvDevice
import requests
import datetime
import dateutils
from .commands import make_conversion
from .api import olltv_auth, olltv_users_list, oll_user_check, oll_user_add, oll_user_bind, oll_user_unbind, oll_user_info, oll_check_bundle, oll_get_device, oll_dev_check, oll_dev_add, oll_disable_bundle, oll_dev_remove, oll_add_bundle, olltv_change_email, olltv_change_userinfo, oll_account_check
from core import module_check

modules = settings.INSTALLED_APPS


def copyf(data, key, allowed):
    return filter(lambda x: key in x and x[key] in allowed, data)


@login_required(login_url='/login/')
def index(request):
    if 'olltv' in modules:
        order_by = request.GET.get('order_by', '-registration')
        iptv_users_list = Iptv.objects.all().order_by(order_by)
        paginator = Paginator(iptv_users_list, settings.IPTV_USERS_PER_PAGE)
        page = request.GET.get('page', 1)
        try:
            iptv = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            iptv = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            iptv = paginator.page(paginator.num_pages)
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
        pre_end = iptv.paginator.num_pages - 2
        return render(request, 'olltv_users_list.html', locals())
    else:
        error = 'No module named <b>OLLTV</b>'
        return render(request, 'index.html', locals())


@login_required(login_url='/login/')
def user_change(request, uid):
    if module_check.check(request, 'olltv'):
        olltv_module = True
    else:
        olltv_module = False
    auth = olltv_auth()
    if auth['status'] != 0:
        error = auth
        messages.error(request, auth)
        return render(request, 'index.html', locals())
    else:
        try:
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            user = False
            messages.error(request, 'User not found')
            return render(request, 'olltv_user.html', locals())
# user_info
        device_add_form = DeviceAddForm(initial={'uid': user.id})
        user_info = oll_user_info(account=user.id, hash=auth['hash'])
        if user_info['status'] == 505:
            messages.warning(request, user_info)
            return render(request, 'olltv_user.html', locals())
        elif user_info['status'] == 404:
# oll_user_check
            check_user = oll_user_check(email=user.email, hash=auth['hash'])
            messages.warning(request, check_user)
            if check_user['data'] == 0:
                if 'save-user' in request.POST:
                    u_add = oll_user_add(request=request, hash=auth['hash'])
                    try:
                        iptv = Iptv.objects.get(uid=user)
                        messages.success(request, u'User %s was created' % user)
                        return redirect('olltv:user_change', uid=user.id)
                    except Iptv.DoesNotExist:
                        iptv = Iptv.objects.create(
                            uid=user,
                            tp_id=69,
                            #mac='',
                            #pin='',
                            disable=1,
                            registration=datetime.date.today()
                        )
                        messages.success(request, u'User %s was created' % user)
                        return redirect('olltv:user_change', uid=user.id)
            else:
# oll_user_bind
                if 'bind-user' in request.POST:
                    u_bind = oll_user_bind(user=user, hash=auth['hash'])
                    if u_bind == True:
                        try:
                            iptv = Iptv.objects.get(uid=user)
                            messages.success(request, u'User %s was binded' % user)
                            return redirect('olltv:user_change', uid=user.id)
                        except Iptv.DoesNotExist:
                            iptv = Iptv.objects.create(
                                uid=user,
                                tp_id=69,
                                #mac='',
                                #pin='',
                                disable=1,
                                registration=datetime.date.today()
                            )
                            messages.success(request, u'User %s was binded' % user)
                            return redirect('olltv:user_change', uid=user.id)
                    else:
                        messages.error(request, u_bind)
            return render(request, 'olltv_user.html', locals())
        else:
# user active
            try:
                iptv = Iptv.objects.get(uid=user.id)
                print iptv.tp_id
                cur_tp = Tp.objects.get(tp_id=iptv.tp_id)
            except Iptv.DoesNotExist:
                iptv = False
                if 'activate-user' in request.POST:
                    iptv = Iptv(
                        uid=user,
                        tp_id=69,
                        #mac='',
                        #pin='',
                        disable=1,
                        registration=datetime.date.today()
                    )
                    iptv.save()
                    return redirect('olltv:user_change', uid=user.id)
                return render(request, 'olltv_user.html', locals())
# get bundle
            get_user_info = user_info['data']
            tp_list_dict = user_info['data']['bought_subs']
            tp_count = user_info['tp_count']
            tp_list = []
            if tp_count < 1:
                tp_list = []
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
# get_devices
            get_devices = oll_get_device(account=user.id, hash=auth['hash'])
            if get_devices['mess'] == 'Error':
                messages.warning(request, get_devices)
            else:
                get_dev_list = get_devices['data']
            account_check = oll_account_check(account=user.id, hash=auth['hash'])
            if account_check['mess'] == 'Error':
                messages.warning(request, account_check)
            else:
                get_account_info = account_check['data']
            TYPE = (
                ('subs_free_device', 'Новый контракт - 24 мес и оборудование за 1 грн'),
                ('subs_buy_device', 'Новый контракт - покупка оборудования'),
                ('subs_rent_device', 'Новый контракт - аренда оборудования'),
                ('subs_no_device', 'Новый контаркт - без оборудования'),
                ('subs_renew', 'Восстановление текущего контракта'),
            )
            DEVICE_TYPE = (
                ('subs_free_device', 'Новый контракт - 24 мес и оборудование за 1 грн'),
                ('subs_buy_device', 'Новый контракт - покупка оборудования'),
                ('subs_rent_device', 'Новый контракт - аренда оборудования'),
                ('subs_no_device', 'Новый контаркт - без оборудования'),
                ('subs_renew', 'Восстановление текущего контракта'),
            )
            if iptv.disable == 1 or iptv.disable == 2:
                tps = Tp.objects.filter(module='iptv').exclude(id=137).order_by('pk')
            else:
                tps = AbonTarifs.objects.filter(id__in=settings.ABONTARIFS)
            bill = Bill.objects.get(uid=user.id)
# bind unbind tp
            type_form = TypeForm()
            device_remove_form = DeviceRemoveForm()
            device_add_form = DeviceAddForm()
            print request.POST
            if 'action' in request.POST:
                auth = olltv_auth()
# unbind-tp
                if request.POST['action'] == 'unbind-tp':
                    type_form = TypeForm(request.POST)
                    admin_log = AdminLog(
                        actions='Unbundle tarif plan %s [%s]' % (request.POST['tpid'], str(request.user.id)),
                        datetime=datetime.datetime.now(),
                        ip=ip_to_num(request.META.get('REMOTE_ADDR')),
                        user=user,
                        admin_id='1',
                        action_type=15,
                        module='Iptv',
                    )
                    oll_unbundle = oll_disable_bundle(account=user.id, sub_id=request.POST['tpid'], type=request.POST['type'], hash=auth['hash'])
                    if oll_unbundle['status'] != 0:
                        messages.error(request, oll_unbundle)
                        return render(request, 'olltv_user.html', locals())
                    else:
                        messages.success(request, oll_unbundle)
                        if not 'tp_type' in request.POST:
                            iptv.tp_id = 69
                            iptv.disable = 2
                            iptv.save()
                        admin_log.save()
                        if 'tp_type' in request.POST and request.POST['tp_type'] == 'extra':
                            abon_tp = AbonTarifs.objects.get(name=request.POST['tpid'])
                            try:
                                abon = AbonUserList.objects.filter(uid=user.id, tp_id=abon_tp.id)
                                abon.delete()
                            except AbonUserList.DoesNotExist:
                                error = 'AbonUserList DoesNotExist'
                        return redirect('olltv:user_change', uid=user.id)
                if request.POST['action'] == 'add-tp':
# add tp
                    if 'now' in request.POST:
                        tp = Tp.objects.get(name=request.POST['tp'])
                        add_bundle = oll_add_bundle(account=user.id, tp=request.POST['tp'], type=request.POST['type'], hash=auth['hash'])
                        if add_bundle['status'] != 0:
                            messages.error(request, add_bundle)
                            return render(request, 'olltv_user.html', locals())
                        else:
                            messages.success(request, add_bundle)
                            fees = Fees.objects.create(
                                date=datetime.datetime.today(),
                                sum=make_conversion(tp.cost),
                                last_deposit=bill.deposit,
                                uid=user,
                                dsc='Activate tarif plan %s (%s)' % (request.POST['tp'], request.user.id),
                                aid_id='1',
                                bill_id=bill.id,
                                method_id=1
                            )
                            admin_log = AdminLog.objects.create(
                                actions='Bundle tarif plan %s [%s]' % (tp.name, str(request.user.id)),
                                datetime=datetime.datetime.now(),
                                ip=ip_to_num(request.META.get('REMOTE_ADDR')),
                                user=user,
                                admin_id='1',
                                action_type=15,
                                module='Iptv',
                            )
                            bill.deposit = bill.deposit - make_conversion(tp.cost)
                            iptv.disable = 0
                            iptv.tp = tp
                            iptv.registration = datetime.date.today()
                            iptv.save()
                            bill.save()
                            return redirect('olltv:user_change', uid=user.id)
                    else:
                        print 'no post'
                if request.POST['action'] == 'add-extra-screen':
# add extra screen
                    if 'now' in request.POST:
                        abon_tp = AbonTarifs.objects.get(name=request.POST['tp'])
                        try:
                            abon = AbonUserList.objects.get(uid=user.id, tp_id=abon_tp.id)
                        except AbonUserList.DoesNotExist:
                            abon = AbonUserList.objects.create(
                                uid=user.id,
                                tp_id=abon_tp.id,
                                date=datetime.date.today(),
                            )
                        add_bundle = oll_add_bundle(account=user.id, tp=request.POST['tp'], type=request.POST['type'], hash=auth['hash'])
                        if add_bundle['status'] != 0:
                            messages.error(request, add_bundle)
                            return render(request, 'olltv_user.html', locals())
                        else:
                            messages.success(request, add_bundle)
                            fees = Fees.objects.create(
                                date=datetime.datetime.today(),
                                sum=make_conversion(abon_tp.price),
                                last_deposit=bill.deposit,
                                uid=user,
                                dsc='Activate tarif plan %s (%s)' % (request.POST['tp'], request.user.id),
                                aid_id='1',
                                bill_id=bill.id,
                                method_id=1
                            )
                            admin_log = AdminLog.objects.create(
                                actions='Bundle extra screen %s [%s]' % (abon_tp.name, str(request.user.id)),
                                datetime=datetime.datetime.now(),
                                ip=ip_to_num(request.META.get('REMOTE_ADDR')),
                                user=user,
                                admin_id='1',
                                action_type=15,
                                module='Iptv',
                            )
                            bill.deposit = bill.deposit - make_conversion(abon_tp.price)
                            bill.save()
                            return redirect('olltv:user_change', uid=user.id)
# dev unbind
                if request.POST['action'] == 'unbind-dev':
                    device_remove_form = DeviceRemoveForm(request.POST)
                    if device_remove_form.is_valid():
                        d_remove = oll_dev_remove(request=request, account=user.id, mac=request.POST['mac'], serial_number=request.POST['serial'], hash=auth['hash'])
                        if d_remove['status'] == 0:
                            messages.success(request, d_remove)
                            admin_log = AdminLog.objects.create(
                                actions='Unbind device mac: %s | serial: %s [%s]' % (request.POST['mac'], request.POST['serial'], str(request.user.id)),
                                datetime=datetime.datetime.now(),
                                ip=ip_to_num(request.META.get('REMOTE_ADDR')),
                                user=user,
                                admin_id='1',
                                action_type=15,
                                module='Iptv',
                            )
                            try:
                                dev = IptvDevice.objects.get(mac=request.POST['mac'], serial_num=request.POST['serial'])
                                dev.status = 1
                                dev.save()
                            except IptvDevice.DoesNotExist:
                                pass
                            return redirect('olltv:user_change', uid=user.id)
                        else:
                            messages.error(request, d_remove)
# dev bind
                if request.POST['action'] == 'bind-dev':
                    device_add_form = DeviceAddForm(request.POST)
                    d_add = oll_dev_add(request=request, account=user.id, hash=auth['hash'])
                    if d_add['status'] == 0:
                        messages.success(request, d_add)
                        dev_type = IptvDeviceType.objects.get(id=request.POST['device_type'])
                        admin_log = AdminLog.objects.create(
                            actions='Bind device mac: %s | serial: %s [%s]' % (request.POST['mac'], request.POST['serial_num'], str(request.user.id)),
                            datetime=datetime.datetime.now(),
                            ip=ip_to_num(request.META.get('REMOTE_ADDR')),
                            user=user,
                            admin_id='1',
                            action_type=15,
                            module='Iptv',
                        )
                        try:
                            dev = IptvDevice.objects.get(mac=request.POST['mac'], serial_num=request.POST['serial_num'])
                            dev.status = 0
                            dev.save()
                        except IptvDevice.DoesNotExist:
                            dev = IptvDevice.objects.create(
                                uid=user,
                                device_type=dev_type,
                                mac=request.POST['mac'],
                                serial_num=request.POST['serial_num'],
                                model=request.POST['model'],
                            )
                        return redirect('olltv:user_change', uid=user.id)
                    else:
                        messages.success(request, d_add)
# change email
                if request.POST['action'] == 'email-change':
                    oll_change_email = olltv_change_email(email=request.POST['email'], new_email=request.POST['new_email'], hash=auth['hash'])
                    messages.success(request, oll_change_email)
                    try:
                        upi = UserPi.objects.get(id=uid)
                        upi.email = request.POST['new_email']
                        upi.save()
                    except UserPi.DoesNotExist:
                        print 'UserPi.DoesNotExist'
                    if settings.ABILLS_EMAIL_LOGS:
                        admin_log = AdminLog(
                            actions='Email changed from %s to %s (%s)' % (request.POST['email'], request.POST['new_email'], request.user.login),
                            datetime=datetime.datetime.now(),
                            ip=ip_to_num(request.META.get('REMOTE_ADDR')),
                            user=user,
                            admin_id='1',
                            action_type=15,
                            module='Iptv',
                        )
                        admin_log.save()
                    return redirect('olltv:user_change', uid=user.id)
# change info
                if request.POST['action'] == 'info-change':
                    oll_change_userinfo = olltv_change_userinfo(request, account=uid, hash=auth['hash'])
                    admin_log = AdminLog(
                        actions='Info changed (%s)' % (request.user.login),
                        datetime=datetime.datetime.now(),
                        ip=ip_to_num(request.META.get('REMOTE_ADDR')),
                        user=user,
                        admin_id='1',
                        action_type=15,
                        module='Iptv',
                    )
                    admin_log.save()
                    return redirect('olltv:user_change', uid=user.id)
# unbind user
                if request.POST['action'] == 'user-unbind':
                    olltv_user_unbind = oll_user_unbind(request, hash=auth['hash'])
                    admin_log = AdminLog(
                        actions='User was unbinded (%s)' % (request.user.login),
                        datetime=datetime.datetime.now(),
                        ip=ip_to_num(request.META.get('REMOTE_ADDR')),
                        user=user,
                        admin_id='1',
                        action_type=15,
                        module='Iptv',
                    )
                    admin_log.save()
                    return redirect('olltv:user_change', uid=user.id)
            return render(request, 'olltv_user.html', locals())


@login_required(login_url='/login/')
def user_remove(request):
    user_add = UserRemoveForm()
    if request.method == 'POST':
        print request.POST
        user_add = UserRemoveForm(request.POST)
        try:
            user = User.objects.get(account=request.POST['account'])
            if request.POST['login'] != user.login:
                pass
            else:
                print 'form error'
                user_add = UserAddForm()
                error = 'user with login %s already there' % request.POST['login']
                return render(request, 'olltv/user_add.html', locals())
        except User.DoesNotExist:
            pass
        if user_add.is_valid():
            print 'form valid'
            vehicle = user_add.save(commit=False)
            vehicle.author = request.user.get_full_name()
            vehicle.account = request.POST['account']
            vehicle.oll_id = 0
            vehicle.save()
            if 'save' in request.POST:
                return redirect(reverse('olltv:index'))
            elif 'save_continue' in request.POST:
                return redirect(reverse('olltv:claim_edit', args=(vehicle.id,)))
            elif 'save_add' in request.POST:
                return redirect(reverse('olltv:user_add'))
        return render(request, 'olltv/user_add.html', locals())
    user_add = UserAddForm()
    return render(request, 'olltv/user_add.html', locals())


@login_required(login_url='/login/')
def get_all_users(request):
    response_auth = requests.post('http://oll.tv/ispAPI/auth2/', data={
        'login': 'mtel',
        'password': 'x_g~-5~(;ZY'
    })
    response_content = response_auth.json()
    #print response_content
    response_get_user_list = requests.post('http://oll.tv/ispAPI/getUserList/', data={
        'offset': '',
        'hash': response_content['hash']
    })
    get_user_list_json = response_get_user_list.json()
    get_user_list = get_user_list_json['data']
    num = 0
    print get_user_list
    for i in get_user_list:
        print str(num) + '. ' + i['account'] + ' ' + i['firstname'] + ' ' + i['lastname'] + ' ' + i['email']
        num = num + 1
        u = User(email=i['email'], account=i['account'], birth_date=i['birth_date'], gender=i['gender'], firstname=i['firstname'], lastname=i['lastname'], phone=i['phone'], region=i['region'], receive_news=i['receive_news'], index=['index'], status=i['active'], registration_date=i['reg_date'], oll_id=i['ID'])
        u.save()
    return render(request, 'olltv/get_all_users.html', locals())


@login_required(login_url='/login/')
def get_all_dev(request):
    response_auth = requests.post('http://oll.tv/ispAPI/auth2/', data={
        'login': 'mtel',
        'password': 'x_g~-5~(;ZY'
    })
    response_content = response_auth.json()
    response_get_user_list = requests.post('http://oll.tv/ispAPI/getDeviceList/', data={
        'offset': '',
        'hash': response_content['hash']
    })
    get_user_list_json = response_get_user_list.json()
    get_user_list = get_user_list_json['data']
    num = 0
    print get_user_list_json['data'][0]
    for i in get_user_list:
        print str(num) + '. ' + i['USER']['account'] + ' ' + i['serial_number']
        num = num + 1
        u = User.objects.get(account=i['USER']['account'])
        print u.account
        #d = Device(account_id=u.pk, mac=i['mac'], serial_number=i['serial_number'], status=1, date_added=i['date_added'], id=i['ID'])
        #d.save()
    return render(request, 'olltv/get_all_dev.html', locals())