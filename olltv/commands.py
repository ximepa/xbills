# -*- coding: utf-8 -*-
__author__ = 'ximepa'
from core.models import User, Dv
import datetime
import calendar


def get_tp_cost(request):
    u = User.objects.get(login=request.user)
    dv = Dv.objects.get(user=u.pk)
    dv.tp_id = request.POST.get('change_tp')
    return dv.tp.cost


def get_tp_cost_admin(request, uid):
    u = User.objects.get(id=uid)
    dv = Dv.objects.get(user=u.pk)
    dv.tp_id = request.POST.get('change_tp')
    return dv.tp.cost


def make_conversion(tp_cost):
    last_day = calendar.monthrange(datetime.date.today().year, datetime.date.today().month)[1]
    one_day_cost = tp_cost / last_day
    today_day = datetime.date.today().day - 1
    suma = today_day * one_day_cost
    delete_amount = tp_cost - suma
    return delete_amount