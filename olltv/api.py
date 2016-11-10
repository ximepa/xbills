# -*- coding: utf-8 -*-
__author__ = 'ximepa'
from django.conf import settings
import requests
import datetime
from django.shortcuts import render, redirect
from .models import IptvDeviceType


class OLLTV:
    def __init__(self, login=settings.OLLTVUSERNAME, password=settings.OLLTVPASSWD):
        # Метод авторизации
        auth = {}
        try:
            response = requests.post(settings.OLLTVUSERAUTH, data={
                'login': login,
                'password': password
            }, timeout=10)
            response_content = response.json()
            auth.update(response_content)
            self.auth = auth
        except requests.RequestException:
            print 'time out'
            auth.update({'status': 21, 'message': 'Time out'})
            self.auth = auth

    def is_auth(self):
        if self.auth['status'] == 0:
            return True
        else:
            return False


    # def get_auth_hash

    # 1. Работа с пользователями
    # 1.1. Метод проверки существования пользователя с данным email в БД oll.tv
    def email_exist(self, email):
        response = requests.post(settings.OLLTVEMILEXISTURL, data={
            'email': email,
            'hash': self.auth['hash'],
        })
        response_content = response.json()
        if response_content['data'] == 1:
            return True
        else:
            return False

    # 1.2. Метод проверки существования пользователя с данным account в БД oll.tv
    def account_exist(self, account):
        print 'account_exist'
        response = requests.post(settings.OLLTVACCOUNTEXISTURL, data={
            'account': account,
            'hash': self.auth['hash'],
        })
        response_content = response.json()
        if response_content['status'] == 0:
            return True
        else:
            return False

    # 1.3. Метод добавления (регистрации) нового пользователя в БД oll.tv
    def user_add(self, email, account, birth_date='1970-01-01', gender='M', firstname='', password='', lastname='', phone='', region='Unknown', receive_news=0, send_registration_email=0, postcode=None):
        print 'user add'
        data = {}
        response = requests.post(settings.OLLTVUSERADDURL, data={
            'email': email,
            'account': account,
            'birth_date': birth_date,
            'gender': gender,
            'firstname': firstname,
            'password': password,
            'lastname': lastname,
            'phone': phone,
            'region': region,
            'receive_news': receive_news,
            'send_registration_email': send_registration_email,
            'index': postcode,
            'hash': self.auth['hash'],
        })
        response_content = response.json()
        data.update(response_content)
        return data

    # 1.4. Метод получения списка пользователей
    def get_users_list(self, offset='', limit=1000, with_subs=0):
        print 'get_users_list'
        data = {}
        response = requests.post(settings.OLLTVUSERLIST, data={
            'offset': '',
            'limit': limit,
            'with_subs': with_subs,
            'hash': self.auth['hash']
        })
        response_content = response.json()
        data.update(response_content)
        return data

    # 1.5. Метод установки/изменения провайдерского аккаунта и привязывания пользователя к провайдеру
    def user_bind(self, email, account):
        print 'user_bind'
        data = {}
        response = requests.post(settings.OLLTVUSERLINKINGURL, data={
            'email': email,
            'account': account,
            'hash': self.auth['hash'],
        })
        response_content = response.json()
        data.update(response_content)
        return data

    # 1.6. Метод отвязки пользователя от оператора
    def user_unbind(self, email, account):
        print 'user unbind'
        data = {}
        response = requests.post(settings.OLLTVUSERREMOVEURL, data={
            'email': email,
            'account': account,
            'hash': self.auth['hash'],
        })
        response_content = response.json()
        data.update(response_content)
        return data

    # 1.7. Метод изменения email
    def email_change(self, email, new_email):
        print 'email_change'
        data = {}
        response = requests.post(settings.OLLTVUSERCHANGEEMAILURL, data={
            'email': email,
            'new_email': new_email,
            'hash': self.auth['hash']
        })
        response_content = response.json()
        data.update(response_content)
        return data

    # 1.8. Метод получения данных о пользователе
    def get_user_info(self, account=None, email=None):
        print 'get_user_info'
        data = {}
        if account:
            response = requests.post(settings.OLLTVUSERINFO, data={
                'account': account,
                'hash': self.auth['hash']
            })
            response_content = response.json()
            data.update({'response': response_content})
            return data
        elif email:
            response = requests.post(settings.OLLTVUSERINFO, data={
                'email': email,
                'hash': self.auth['hash']
            })
            response_content = response.json()
            data.update({'response': response_content})
            return data

    # 1.9. Метод изменения пользовательских данных
    def change_user_info(self, account, birth_date, gender, password, firstname, lastname, phone, region, postcode, multicast=0):
        data = {}
        response = requests.post(settings.OLLTVCHANGEUSERINFO, data={
            'account': account,
            'birth_date': birth_date,
            'gender': gender,
            'password': password,
            'firstname': firstname,
            'lastname': lastname,
            'phone': phone,
            'region': region,
            'index': postcode,
            'multicast': multicast,
            'hash': self.auth['hash'],
        })
        response_content = response.json()
        data.update({'responce': response_content, 'mess_status': 'danger'})
        return data

    # 1.10. Метод сброса пароля родительского контроля
    def parent_control_reset(self, account, email):
        data = {}
        if account:
            response = requests.post(settings.OLLTVPARENTCOONTROLRESET, data={
                'account': account,
                'hash': self.auth['hash'],
            })
            response_content = response.json()
            data.update(response_content)
            return data
        elif email:
            response = requests.post(settings.OLLTVPARENTCOONTROLRESET, data={
                'email': email,
                'hash': self.auth['hash'],
            })
            response_content = response.json()
            data.update(response_content)
            return data

    # 2. Работа с подписками
    # 2.1. Метод включения пользователю бандл-подписки
    def bundle_add(self, account, tp, type):
        data = {}
        response = requests.post(settings.OLLTVTPACTIVATEURL, data={
            'account': account,
            'sub_id': tp,
            'type': type,
            'hash': self.auth['hash'],
        })
        response_content = response.json()
        data.update(response_content)
        return data

    # 2.2. Метод выключения у пользователя бандл-подписки
    def bundle_remove(self, account, tp, type):
        data = {}
        response = requests.post(settings.OLLTVTPDEACTIVATEURL, data={
            'account': account,
            'sub_id': tp,
            'type': type,
            'hash': self.auth['hash']
        })
        response_content = response.json()
        data.update(response_content)
        return data


    # 2.3. Метод проверки состояния бандл-подписки у пользователя
    def bundle_check(self, account, tp):
        data = {}
        response = requests.post(settings.OLLTVGETBUNDLESTATUS, data={
            'account': account,
            'sub_id': tp,
            'hash': self.auth['hash']
        })
        response_content = response.json()
        data.update(response_content)
        return data

    # 2.4. Метод смены у пользователя бандл-подписки
    def bundle_change(self, account, old_tp, new_tp):
        data = {}
        response = requests.post(settings.OLLTVTPCHANGEURL, data={
            'account': account,
            'old_sub_id': old_tp,
            'new_sub_id': new_tp,
            'hash': self.auth['hash']
        })
        response_content = response.json()
        data.update(response_content)
        return data

    # 2.5. Метод получения списка активных подписок провайдера за период
    def get_all_purchases(self, start_date, page=0):
        data = {}
        response = requests.post(settings.OLLTVGETALLPURCHASESURL, data={
            'start_date': start_date,
            'page': page,
            'hash': self.auth['hash']
        })
        response_content = response.json()
        data.update(response_content)
        return data

    # 3. Работа с устройствами
    # 3.1. Метод добавления и привязки нового устройства пользователю
    def device_add(self, account, serial_number, mac, device_type, device_model, type):
        data = {}
        response = requests.post(settings.OLLTVDEVADDURL, data={
            'account': account,
            'serial_number': serial_number,
            'mac': mac,
            'device_type': device_type,
            # 'device_model': device_model,
            # 'binding_code': binding_code,
            'type': type,
            'hash': self.auth['hash']
        })
        response_content = response.json()
        data.update(response_content)
        return data

    # 3.2. Метод отвязки существующего устройства от пользователя
    def device_rem(self, account, mac, serial_number, type):
        data = {}
        response = requests.post(settings.OLLTVDEVREMOVEURL, data={
            'account': account,
            'mac': mac,
            'serial_number': serial_number,
            'type': type,
            'hash': self.auth['hash']
        })
        response_content = response.json()
        data.update(response_content)
        return data

    # 3.3. Метод проверки существования устройства в БД oll.tv
    def device_check(self, mac, serial_number):
        data = {}
        response = requests.post(settings.OLLTVDEVEXISTURL, data={
            'mac': mac,
            'serial_number': serial_number,
            'hash': self.auth['hash']
        })
        response_content = response.json()
        data.update(response_content)
        return data

    # 3.4. Метод получения списка устройств
    def devices_get_list(self, account, offset=''):
        data = {}
        response = requests.post(settings.OLLTVDEVGETLIST, data={
            'account': account,
            'offset': offset,
            'hash': self.auth['hash']
        })
        response_content = response.json()
        data.update(response_content)
        return data

    # 3.5. Метод получения списка устройств абонента с описанием устройств\
    def get_user_devices(self, account=None, email=None):
        data = {}
        if account:
            response = requests.post(settings.OLLTVDEVGETLIST, data={
                'account': account,
                'hash': self.auth['hash']
            })
            response_content = response.json()
            data.update(response_content)
            return data
        elif email:
            response = requests.post(settings.OLLTVDEVGETLIST, data={
                'email': email,
                'hash': self.auth['hash']
            })
            response_content = response.json()
            data.update(response_content)
            return data