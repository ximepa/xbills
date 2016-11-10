# -*- encoding: utf-8 -*-
#from django.contrib.auth.models import check_password
from django.contrib.auth.hashers import check_password

from .models import Admin


class AuthBackend(object):

    def authenticate(self, username=None, password=None):
        try:
            admin = Admin.objects.get(login=username)
            pwd_valid = check_password(password, admin.password)
            if pwd_valid:
                return admin
            else:
                return None
        except Admin.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Admin.objects.get(pk=user_id)
        except Admin.DoesNotExist:
            return None