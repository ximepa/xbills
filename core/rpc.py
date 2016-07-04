# -*- encoding: utf-8 -*-
__author__ = 'ximepa'
from djangorpc import RpcRouter, Msg, Error
from .models import District, Street, House


class MainApiClass(object):

    def hello(self, username, user):
        return Msg(u'Hello, %s!' % username)

    def find_street(self, term, district, user):
        return [s['name'] for s in list(Street.objects.filter(name__icontains=term, district__name=district).values('name')[:10])]

    def find_build(self, term, street, user):
        return [b['number'] for b in list(House.objects.filter(number__icontains=term, street__name=street).values('number')[:10])]

    def find_street1(self, district, user):
        try:
            streets = Street.objects.filter(district__name__iexact=district)
            for s in streets:
                print s.name
        except Street.DoesNotExist:
            return Error('user `%s` not found' % district)
        else:
            return {
                'success': True,
                'pk': s.pk,
                'login': s.name,
            }

rpc_router = RpcRouter({
    'MainApi': MainApiClass(),
})