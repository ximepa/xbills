# -*- coding: utf-8 -*-
__author__ = 'ximepa'
from django.conf import settings
import requests
import datetime
from django.shortcuts import render, redirect
from .models import IptvDeviceType

# Метод авторизации
def olltv_auth():
    data = {}
    response_auth = requests.post(settings.OLLTVUSERAUTH, data={
        'login': settings.OLLTVUSERNAME,
        'password': settings.OLLTVPASSWD
    })
    response_content = response_auth.json()
    if response_content['status'] == 0:
        data = {'hash': response_content['hash'], 'status': response_content['status'], 'mess': 'Authentification successfull'}
        return data
    else:
        data.update(response_content)
        data.update({'mess': 'Error'})
        return response_content


# 1. Работа с пользователями
# 1.1. Метод проверки существования пользователя с данным email в БД oll.tv
def oll_user_check(email, hash):
    data = {}
    response_user_check = requests.post(settings.OLLTVEMILEXISTURL, data={
        'email': email,
        'hash': hash,
    })
    user_check_content = response_user_check.json()
    if user_check_content['data'] == 1:
        data.update(user_check_content)
        data.update({'mess': u'User %s exist' % (email,), 'mess_status': 'danger'})
        return data
    else:
        data.update(user_check_content)
        data.update({'mess': u'User %s not exist' % (email,), 'mess_status': 'success'})
        return data


# 1.2. Метод проверки существования пользователя с данным email в БД oll.tv
def oll_account_check(account, hash):
    data = {}
    response_user_check = requests.post(settings.OLLTVACCOUNTEXISTURL, data={
        'account': account,
        'hash': hash,
    })
    user_check_content = response_user_check.json()
    if user_check_content['status'] == 0:
        data.update(user_check_content)
        data.update({'mess': u'Користувач %s існує' % (account,), 'mess_status': 'success', 'module': 'User info'})
        return data
    else:
        data.update(user_check_content)
        data.update({'mess': u'Error', 'mess_status': 'danger', 'module': 'User info'})
        return data


# 1.3. Метод добавления (регистрации) нового пользователя в БД oll.tv
def oll_user_add(request, hash):
    data = {}
    if request.method == 'POST':
        response_user_reg = requests.post(settings.OLLTVUSERADDURL, data={
            'email': request.POST['email'],
            'account': request.POST['account'],
            'birth_date': request.POST['birth_date'],
            'gender': request.POST['gender'],
            'firstname': request.POST['firstname'],
            'password': request.POST['password'],
            'lastname': request.POST['lastname'],
            'phone': request.POST['phone'],
            'region': request.POST['region'],
            'receive_news': request.POST['receive_news'],
            'send_registration_email': request.POST['send_registration_email'],
            'index': request.POST['postcode'],
            'hash': hash,
        })
        user_reg_content = response_user_reg.json()
        if user_reg_content['status'] != 0:
            data.update(user_reg_content)
            data.update({'mess': str(user_reg_content), 'mess_status': 'danger'})
            return data
    return True


# 1.4. Метод получения списка пользователей
def olltv_users_list(hash):
    data = {}
    response_get_user_list = requests.post(settings.OLLTVUSERLIST, data={
        'offset': '',
        'hash': hash
    })
    response_content = response_get_user_list.json()
    if response_content['status'] == 0:
        data.update(response_content)
        data.update({'mess': 'Userlist success'})
        return data
    else:
        data.update(response_content)
        data.update({'mess': 'Error'})
        return data


# 1.5. Метод установки/изменения провайдерского аккаунта и привязывания пользователя к провайдеру
def oll_user_bind(user, hash):
    data = {}
    response_user_link = requests.post(settings.OLLTVUSERLINKINGURL, data={
        'email': user.email,
        'account': user.id,
        'hash': hash,
    })
    user_link_content = response_user_link.json()
    if user_link_content['status'] != 0:
        data.update(user_link_content)
        data.update({'mess': str(user_link_content), 'mess_status': 'danger'})
        return data
    return True


# 1.6. Метод отвязки пользователя от оператора
def oll_user_unbind(request, hash):
    data = {}
    if request.method == 'POST':
        response_user_link = requests.post(settings.OLLTVUSERREMOVEURL, data={
            'email': request.POST['email'],
            'account': request.POST['account'],
            'hash': hash,
        })
        user_link_content = response_user_link.json()
        if user_link_content['status'] != 0:
            data.update(user_link_content)
            data.update({'mess': str(user_link_content), 'mess_status': 'danger'})
            return data
    return True


# 1.7. Метод изменения email
def olltv_change_email(email, new_email, hash):
    data = {}
    response_get_user_list = requests.post(settings.OLLTVUSERCHANGEEMAILURL, data={
        'email': email,
        'new_email': new_email,
        'hash': hash
    })
    response_content = response_get_user_list.json()
    if response_content['status'] == 0:
        data.update(response_content)
        data.update({'mess': 'Email change'})
        return data
    else:
        data.update(response_content)
        data.update({'mess': 'Error'})
        return data


# 1.8. Метод получения данных о пользователе
def oll_user_info(account, hash):
    data = {}
    response_get_user_info = requests.post(settings.OLLTVUSERINFO, data={
        'account': account,
        'hash': hash
    })
    get_user_info_json = response_get_user_info.json()
    if get_user_info_json['status'] != 0:
        data.update(get_user_info_json)
        data.update({'mess': 'Error', 'mess_status': 'danger', 'module': 'User info'})
        return data
    else:
        data.update(get_user_info_json)
        data.update({'mess': u'User info get successfull', 'mess_status': 'success', 'module': 'User info', 'tp_count': len(get_user_info_json['data']['bought_subs'])})
        return data


# 1.9. Метод изменения пользовательских данных
def olltv_change_userinfo(request, account, hash):
    data = {}
    if request.method == 'POST':
        response_user_reg = requests.post(settings.OLLTVCHANGEUSERINFO, data={
            'account': account,
            'birth_date': request.POST['birth_date'],
            'gender': request.POST['gender'],
            'password': request.POST['password'],
            'firstname': request.POST['firstname'],
            'lastname': request.POST['lastname'],
            'phone': request.POST['phone'],
            'region': request.POST['region'],
            'index': request.POST['index'],
            'hash': hash,
        })
        user_reg_content = response_user_reg.json()
        if user_reg_content['status'] != 0:
            data.update(user_reg_content)
            data.update({'mess': str(user_reg_content), 'mess_status': 'danger'})
            return data
    return True


# 2. Работа с подписками
# 2.1. Метод включения пользователю бандл-подписки
def oll_add_bundle(account, tp, type, hash):
    data = {}
    response_add_bundle = requests.post(settings.OLLTVTPACTIVATEURL, data={
        'account': account,
        'sub_id': tp,
        'type': type,
        'hash': hash,
    })
    response_add_bundle_json = response_add_bundle.json()
    if response_add_bundle_json['status'] != 0:
        data.update(response_add_bundle_json)
        data.update({'mess': 'Error', 'mess_status': 'danger', 'module': 'Bundle'})
        return data
    else:
        data.update(response_add_bundle_json)
        data.update({'mess': u'Bundle added successfull', 'mess_status': 'success', 'module': 'Bundle'})
        return data


# 2.2. Метод выключения у пользователя бандл-подписки
def oll_disable_bundle(account, sub_id, type, hash):
    data = {}
    response_get_bundle_status = requests.post(settings.OLLTVTPDEACTIVATEURL, data={
        'account': account,
        'sub_id': sub_id,
        'type': type,
        'hash': hash
    })
    get_bundle_status_json = response_get_bundle_status.json()
    if get_bundle_status_json['status'] != 0:
        data.update(get_bundle_status_json)
        data.update({'mess': 'Error', 'mess_status': 'danger', 'module': 'Bundle'})
        return data
    else:
        data.update(get_bundle_status_json)
        data.update({'mess': u'TP unbundle successfull', 'mess_status': 'success', 'module': 'Bundle'})
        return data


# 2.3. Метод проверки состояния бандл-подписки у пользователя
def oll_check_bundle(account, tp, hash):
    data = {}
    response_get_bundle_status = requests.post(settings.OLLTVGETBUNDLESTATUS, data={
        'account': account,
        'sub_id': tp,
        'hash': hash
    })
    get_bundle_status_json = response_get_bundle_status.json()
    print get_bundle_status_json
    if get_bundle_status_json['status'] != 0:
        data.update(get_bundle_status_json)
        data.update({'mess': 'Error', 'mess_status': 'danger', 'module': 'Bundle'})
        return data
    else:
        data.update(get_bundle_status_json)
        data.update({'mess': u'User bundle get successfull', 'mess_status': 'success', 'module': 'Bundle'})
        return data


# 3. Работа с устройствами
# 3.1. Метод добавления и привязки нового устройства пользователю
def oll_dev_add(request, account, hash):
    data = {}
    dev_type = IptvDeviceType.objects.get(id=request.POST['device_type'])
    response_dev_add = requests.post(settings.OLLTVDEVADDURL, data={
        'account': account,
        'serial_number': request.POST['serial_num'],
        'mac': request.POST['mac'],
        'device_type': dev_type.name,
        'device_model': request.POST['model'],
        #'binding_code': request.POST['binding_code'],
        'type': request.POST['type'],
        'hash': hash,
    })
    dev_add_content = response_dev_add.json()
    if dev_add_content['status'] != 0:
        data.update(dev_add_content)
        data.update({'mess': 'Error', 'mess_status': 'danger', 'module': 'Bundle'})
        return data
    else:
        data.update(dev_add_content)
        data.update({'mess': u'Device bind successfull', 'mess_status': 'success', 'module': 'Bundle'})
        return data


# 3.2. Метод отвязки существующего устройства от пользователя
def oll_dev_remove(request, mac, serial_number, account, hash):
    data = {}
    response_dev_add = requests.post(settings.OLLTVDEVREMOVEURL, data={
        'account': account,
        'mac': mac,
        'serial_number': serial_number,
        'type': request.POST['type'],
        'hash': hash,
    })
    dev_remove_content = response_dev_add.json()
    if dev_remove_content['status'] != 0:
        data.update(dev_remove_content)
        data.update({'mess': 'Error', 'mess_status': 'danger', 'module': 'Bundle'})
        return data
    else:
        data.update(dev_remove_content)
        data.update({'mess': u'Device unbind successfull', 'mess_status': 'success', 'module': 'Bundle'})
        return data


# 3.3. Метод проверки существования устройства в БД oll.tv
def oll_dev_check(mac, serial_number, hash):
    data = {}
    response_user_check = requests.post(settings.OLLTVDEVEXISTURL, data={
        'mac': mac,
        'serial_number': serial_number,
        'hash': hash,
    })
    user_check_content = response_user_check.json()
    if user_check_content['data'] != 0:
        data.update(user_check_content)
        data.update({'mess': u'Пристрій (mac - %s, serial_number - %s) існує' % (mac, serial_number), 'mess_status': 'danger', 'module': 'Devices check'})
        return data
    else:
        data.update(user_check_content)
        data.update({'mess': u'Пристрій (mac - %s, serial_number - %s) не існує' % (mac, serial_number), 'mess_status': 'success', 'module': 'Devices check'})
        return data


# 3.4. Метод получения списка устройств
def oll_get_device(account, hash):
    data = {}
    response_get_dev_list = requests.post(settings.OLLTVDEVGETLIST, data={
        'account': account,
        'offset': '',
        'hash': hash
    })
    get_dev_list_json = response_get_dev_list.json()
    if get_dev_list_json['data'] == []:
        data.update(get_dev_list_json)
        data.update({'mess': 'Error', 'mess_status': 'warning', 'module': 'Devices'})
        return data
    else:
        data.update(get_dev_list_json)
        data.update({'mess': u'User devices get successfull', 'mess_status': 'success', 'module': 'Devices'})
        return data