# -*- encoding: utf-8 -*-
from django.db import models
import os
import datetime
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
)
from django.db import connection
from django.conf import settings

__author__ = 'ximepa'


def ip_to_num(ip_addr):
    sets = map(int, ip_addr.split("."))
    return int(sets[0]*256**3 + sets[1]*256**2 + sets[2]*256 + sets[3])

def num_to_ip(number):
    d = number % 256
    c = int(number/256) % 256
    b = int(number/(256**2)) % 256
    a = int(number/(256**3)) % 256
    return "%s.%s.%s.%s" % (a,b,c,d)


class Admin(AbstractBaseUser):
    login = models.CharField(max_length=50, db_column='id', unique=True)
    name = models.CharField(max_length=50, db_column='name')
    id = models.AutoField(unique=True, primary_key=True, db_column='aid')
    regdate = models.DateField(auto_now_add=True, db_column='regdate')
    disable = models.BooleanField(default=0, db_column='disable', blank=True)
    theme = models.CharField(max_length=40, default='default', choices=[(str(o), str(o)) for o in os.listdir('static') if not o.startswith('custom')])
    phone = models.CharField(max_length=20, db_column='phone', blank=True)
    cell_phone = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=35, blank=True)
    address = models.CharField(max_length=60, blank=True)
    objects = BaseUserManager()
    #last_login = models.DateTimeField(blank=True, null=True, db_column='last_login')
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return str(self.id)

    @property
    def get_hash_password(self):
        q = 'SELECT aid, DECODE(password, "%s") as pwd FROM %s WHERE aid=%s' % (settings.ENCRYPT_KEY, self._meta.db_table, self.id)
        return self.__class__.objects.raw(q)[0].pwd

    @get_hash_password.setter
    def get_hash_password(self, value):
        print value
        cursor = connection.cursor()
        q = 'SELECT ENCODE("%s", "%s") as pwd' % (value, settings.ENCRYPT_KEY)
        cursor.execute(q)
        row = cursor.fetchone()
        self.password = row[0]

    def get_full_name(self):
        return str(self.login)


    class Meta:
        db_table = 'admins'
        ordering = ['id']


class Admin_Settings(models.Model):

    aid = models.SmallIntegerField(primary_key=True, default=0)
    object = models.CharField(primary_key=True, max_length=20)
    setting = models.TextField

    def __unicode__(self):
        return "%s" % self.aid

    class Meta:
        db_table = 'admin_settings'



class Bill(models.Model):

    deposit = models.FloatField(default=0)
    uid = models.IntegerField(blank=True, null=True)
    company_id =models.IntegerField(blank=True, null=True)
    registration = models.DateField(auto_now_add=True)
    #sync = models.FloatField(default=0)
    #linked = models.BooleanField(default=0)

    def __unicode__(self):
        return "%s" % self.deposit

    class Meta:
        db_table = 'bills'


class Company(models.Model):

    bill = models.ForeignKey(Bill, related_name='companies')
    name = models.CharField(max_length=100, unique=True)
    credit = models.FloatField(default=0)
    credit_date = models.DateField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'companies'
        ordering = ['name']


class User(models.Model):

    id = models.IntegerField(primary_key=True, db_column='uid')
    login = models.CharField(max_length=20, unique=True, db_column='id')
    disabled = models.BooleanField(db_column='disable')
    company = models.ForeignKey(Company, related_name='clients')
    credit = models.FloatField(db_column='credit', default='0.00', blank=True, null=False)
    credit_date = models.DateField(db_column='credit_date', default='0000-00-00', blank=True)
    gid = models.ForeignKey('Group', db_column='gid', related_name='user_group')
    reduction = models.FloatField(db_column='reduction', default='0.00', blank=True)
    reduction_date = models.DateField(db_column='reduction_date', default='0000-00-00', blank=True)
    activate = models.DateField(db_column='activate', default='0000-00-00', blank=True)
    expire = models.DateField(db_column='expire', default='0000-00-00', blank=True)
    deleted = models.BooleanField(db_column='deleted')
    bill = models.ForeignKey('Bill')

    def __unicode__(self):
        return self.login

    class Meta:
        db_table = 'users'
        ordering = ['id']

    # @property
    # def bill(self):
    #     try:
    #         c = Company.objects.get(id=self.company.id)
    #         return Bill.objects.get(company_id=c.id)
    #     except Company.DoesNotExist:
    #         try:
    #             return Bill.objects.get(uid=self.id)
    #         except Bill.DoesNotExist:
    #             return None


    @property
    def pi(self):
        try:
            return UserPi.objects.get(user_id=self.id)
        except UserPi.DoesNotExist:
            return None

    @property
    def email(self):
        return self.login + '@m-tel.net'

    @property
    def get_hash_password(self):
        q = 'SELECT uid, DECODE(password, "%s") as pwd FROM %s WHERE uid=%s' % (settings.ENCRYPT_KEY, self._meta.db_table, self.id)
        return self.__class__.objects.raw(q)[0].pwd

    @get_hash_password.setter
    def get_hash_password(self, value):
        cursor = connection.cursor()
        q = 'SELECT ENCODE("%s", "%s") as pwd' % (value, settings.ENCRYPT_KEY)
        cursor.execute(q)
        row = cursor.fetchone()
        self.password = row[0]


class Group(models.Model):
    id = models.AutoField(primary_key=True, db_column='gid')
    name = models.CharField(max_length=50)
    descr = models.CharField(max_length=200)

    def __unicode__(self):
        return str(self.id) + ':' + self.name

    class Meta:
        db_table = 'groups'
        ordering = ['id']


class District(models.Model):

    id = models.SmallIntegerField(default=0, db_column='id', primary_key=True)
    name = models.CharField(max_length=120,unique=True, db_column='name')
    zip = models.CharField(max_length=100)
    city = models.CharField(max_length=300)

    def __unicode__(self):
        return self.name


    class Meta:
        db_table = 'districts'
        ordering = ['id']


class Street(models.Model):

    id = models.SmallIntegerField(default=0, db_column='id', primary_key=True)
    district = models.ForeignKey('District')
    name = models.CharField(max_length=120, unique=True, db_column='name')
    # district = models.ForeignKey('District')

    def __unicode__(self):
        return self.name


    class Meta:
        db_table = 'streets'
        ordering = ['id']


class House(models.Model):

    id = models.AutoField(max_length=11, primary_key=True)
    number = models.CharField(max_length=10, db_column='number')
    street = models.ForeignKey('Street', related_name='houses')

    def __unicode__(self):
        return self.number

    class Meta:
        db_table = 'builds'
        ordering = ['id']


class AbonTarifs(models.Model):

    name = models.CharField(max_length=120, blank=True, null=True, default='')
    price = models.FloatField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'abon_tariffs'
        ordering = ['name']


class AbonUserList(models.Model):

    uid = models.CharField(max_length=120, blank=True, default='', primary_key=True)
    tp = models.ForeignKey('AbonTarifs')
    date = models.DateField(default='')

    def __unicode__(self):
        return self.tp.name

    class Meta:
        managed = False
        db_table = 'abon_user_list'
        unique_together = (('uid', 'tp'),)
        ordering = ['uid']


class UserPi(models.Model):

    user_id = models.OneToOneField('User', related_name="user_pi", primary_key=True, db_column='uid', unique=True)
    fio = models.CharField(max_length=100, unique=True)
    #house = models.ForeignKey('House', max_length=100, db_column='address_build', blank=True, default='0')
    email = models.EmailField(db_column='email')
    street = models.ForeignKey('Street', max_length=100, db_column='address_street')
    kv = models.CharField(max_length=10, db_column='address_flat')
    phone = models.CharField(max_length=100, db_column='phone')
    phone2 = models.CharField(max_length=100, db_column='phone2')
    city = models.CharField(max_length=100, db_column='city')
    location = models.ForeignKey('House', db_column='location_id', related_name='location', blank=True, default='0')
    contract_date = models.DateField(db_column='contract_date')

    @property
    def pi(self):
        try:
            return User.objects.get(login=self.user_id)
        except User.DoesNotExist:
            return None

    def __unicode__(self):
        return '%s' % self.user_id

    class Meta:
        db_table = 'users_pi'
        ordering = ['user_id']

    def export(self):
        data = {'exists':True}
        data.update({'fio': self.fio})
        data.update({'street': self.street.name})
        data.update({'house': self.house.number})
        data.update({'kv': self.kv})
        return data


class Payment(models.Model):

    date = models.DateTimeField(default=datetime.datetime.now)
    sum = models.FloatField(default=0)
    aid = models.ForeignKey(Admin,db_column='aid')
    uid = models.ForeignKey('User', db_column='uid')
    bill = models.ForeignKey(Bill,related_name='payments')
    ip = models.IntegerField(default=ip_to_num('127.0.0.1'))
    last_deposit = models.FloatField(default=0)
    dsc = models.CharField(max_length=80, db_column='dsc')
    method = models.IntegerField(db_column='method')

    class Meta:
        db_table = 'payments'
        ordering = ['date']

    def __unicode__(self):
        return '%s' % (self.sum,)

    def ip_to_num(self, ip_addr):
        sets = map(int, ip_addr.split("."))
        return int(sets[0]*256**3 + sets[1]*256**2 + sets[2]*256 + sets[3])

    def num_to_ip(self, number):
        d = number % 256
        c = int(number/256) % 256
        b = int(number/(256**2)) % 256
        a = int(number/(256**3)) % 256
        return "%s.%s.%s.%s" % (a,b,c,d)

    def get_ip(self):
        return self.num_to_ip(self.ip)


class Tp(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=120,unique=True)
    module = models.CharField(max_length=120)
    tp_id = models.IntegerField()
    cost = models.PositiveIntegerField(db_column='month_fee')
    gid = models.ForeignKey('TpGroups', db_column='gid')

    class Meta:
        db_table = 'tarif_plans'
        ordering = ['name']

    def __unicode__(self):
        return str(self.name)

    @classmethod
    def choices(cls):
        res = []
        for obj in cls.objects.all().order_by('pk'):
            res.append((obj.pk, '%s: %s' % (obj.pk, obj.name)))
        return res

    @classmethod
    def iptv_choices(cls):
        res = []
        for obj in cls.objects.filter(module='iptv').order_by('pk'):
            res.append((obj.pk,"%s: %s" % (obj.pk, obj.name)))
        return res


class Dv(models.Model):

    user = models.OneToOneField(User, db_column='uid', related_name="dv", primary_key=True)
    cid = models.CharField(max_length=120, db_column='cid')
    speed = models.CharField(max_length=120, db_column='speed')
    ip = models.IntegerField(db_column='ip')
    netmask = models.IntegerField(db_column='netmask')
    logins = models.IntegerField(db_column='logins')
    filter_id = models.CharField(max_length=120, db_column='filter_id')
    tp = models.ForeignKey(Tp)

    class Meta:
        db_table = 'dv_main'
        ordering = ['user__login']

    def __unicode__(self):
        return "%s - %s" % (self.user.login, self.tp.name)


class ErrorsLog(models.Model):
    nas_id = models.IntegerField(primary_key=True, db_column='nas_id')
    user = models.CharField(max_length=20, db_column='user')
    message = models.CharField(max_length=120, db_column='message')
    date = models.DateTimeField(db_column='date', null=False)
    action = models.CharField(max_length=10, db_column='action', null=False)
    log_type = models.SmallIntegerField(null=False, db_column='log_type')


    @property
    def nas_info(self):
        try:
            return Nas.objects.get(id=self.nas_id)
        except Nas.DoesNotExist:
            return None


    class Meta:
        db_table = 'errors_log'
        ordering = ['user']

    def __unicode__(self):
        return str(self.message)



class Nas(models.Model):
    id = models.SmallIntegerField(default=0, db_column='id', primary_key=True)
    name = models.CharField(max_length=30, db_column='name')
    nas_identifier = models.CharField(max_length=20, db_column='nas_identifier')
    descr = models.CharField(max_length=250, db_column='descr')
    ip = models.CharField(max_length=15, db_column='ip')
    nas_type = models.CharField(max_length=20, db_column='nas_type')
    auth_type = models.SmallIntegerField(default=0, db_column='auth_type')
    mng_host_port = models.CharField(max_length=25, db_column='mng_host_port')
    mng_user = models.CharField(max_length=20, db_column='mng_user')
    rad_pairs = models.TextField(db_column='rad_pairs')
    alive = models.SmallIntegerField(default=0, db_column='alive')
    disable = models.SmallIntegerField(default=0, db_column='disable')
    ext_acct = models.SmallIntegerField(default=0, db_column='ext_acct')
    domain_id = models.SmallIntegerField(default=0, db_column='domain_id')
    address_street = models.CharField(max_length=100, db_column='address_street')
    address_build = models.CharField(max_length=10, db_column='address_build')
    address_flat = models.CharField(max_length=10, db_column='address_flat')
    zip = models.CharField(max_length=7, db_column='zip')
    city = models.CharField(max_length=20, db_column='city')
    gid = models.SmallIntegerField(default=0, db_column='gid')
    country = models.SmallIntegerField(default=0, db_column='country')
    mac = models.CharField(max_length=17, db_column='mac')
    changed = models.DateField(default='0000-00-00 00:00:00', db_column='changed')
    location_id = models.IntegerField(default=0, db_column='location_id')

    class Meta:
        db_table = 'nas'
        ordering = ['id']

    def __unicode__(self):
        return str(self.id)

    @property
    def get_hash_password(self):
        q = 'SELECT id, DECODE(mng_password, "%s") as pwd FROM %s WHERE id=%s' % (
        settings.ENCRYPT_KEY, self._meta.db_table, self.id)
        return self.__class__.objects.raw(q)[0].pwd

class Dv_log(models.Model):
    start = models.DateTimeField(default='0000-00-00 00:00:00', primary_key=True)
    duration = models.IntegerField(default=0)
    sent = models.IntegerField(default=0)
    recv = models.IntegerField(default=0)
    sum = models.FloatField(default='0.000000')
    port_id = models.SmallIntegerField(default=0)
    nas_id = models.SmallIntegerField(default=0)
    ip = models.IntegerField(default=0)
    uid = models.IntegerField()
    tp_id = models.SmallIntegerField(default=0)
    CID = models.CharField(max_length=18)
    acct_input_gigawords = models.SmallIntegerField(default=0, db_column='acct_input_gigawords')
    acct_output_gigawords = models.SmallIntegerField(default=0, db_column='acct_output_gigawords')


    @property
    def nas_info(self):
        try:
            return Nas.objects.get(id=self.nas_id)
        except Nas.DoesNotExist:
            return None


    class Meta:
        db_table = 'dv_log'
        ordering = ['duration']

    def __unicode__(self):
        return str(self.start)

class Dv_calls(models.Model):
    status = models.IntegerField(default=0, db_column='status')
    user_name = models.CharField(max_length=32, db_column='user_name')
    started = models.DateField(default='0000-00-00 00:00:00', db_column='started')
    nas_ip_address = models.IntegerField(default=0, db_column='nas_ip_address')
    nas_port_id = models.IntegerField(default=0, db_column='nas_port_id')
    nas = models.ForeignKey('Nas', db_column='nas_id')
    acct_session_id = models.CharField(max_length=25, db_column='acct_session_id', primary_key=True)
    acct_session_time = models.IntegerField(default=0, db_column='acct_session_time')
    acct_input_octets = models.BigIntegerField(default=0, db_column='acct_input_octets')
    acct_output_octets = models.BigIntegerField(default=0, db_column='acct_output_octets')
    ex_input_octets = models.BigIntegerField(default=0, db_column='ex_input_octets')
    ex_output_octets = models.BigIntegerField(default=0, db_column='ex_output_octets')
    connect_term_reason = models.IntegerField(default=0, db_column='connect_term_reason')
    framed_ip_address = models.IntegerField(default=0, db_column='framed_ip_address')
    lupdated = models.IntegerField(default=0, db_column='lupdated')
    sum = models.FloatField(default='0.0', db_column='sum')
    CID = models.CharField(max_length=18, db_column='CID')
    CONNECT_INFO = models.CharField(max_length=30, db_column='CONNECT_INFO')
    tp_id = models.SmallIntegerField(default=0, db_column='tp_id')
    #nas_id = models.SmallIntegerField(default=0, db_column='nas_id')
    acct_input_gigawords = models.SmallIntegerField(default=0, db_column='acct_input_gigawords')
    acct_output_gigawords = models.SmallIntegerField(default=0, db_column='acct_output_gigawords')
    ex_input_octets_gigawords = models.SmallIntegerField(default=0, db_column='ex_input_octets_gigawords')
    ex_output_octets_gigawords = models.SmallIntegerField(default=0, db_column='ex_output_octets_gigawords')
    uid = models.ForeignKey('User', db_column='uid')
    join_service = models.IntegerField(default=0, db_column='join_service')
    turbo_mode = models.CharField(max_length=30, db_column='turbo_mode')
    guest = models.SmallIntegerField(default=0, db_column='guest')
    framed_interface_id = models.BinaryField(db_column='framed_interface_id')
    framed_ipv6_prefix = models.BinaryField(db_column='framed_ipv6_prefix')


    class Meta:
        db_table = 'dv_calls'
        ordering = ['user_name']

    def __unicode__(self):
        return str(self.uid)


class TpGroups(models.Model):

    name = models.CharField(max_length=120, db_column='name')

    class Meta:
        db_table = 'tp_groups'
        ordering = ['name']

    def __unicode__(self):
        return self.name



class AdminLog(models.Model):
    actions = models.CharField(max_length=120)
    datetime = models.DateTimeField(default=datetime.datetime.now)
    ip = models.IntegerField(default=ip_to_num('127.0.0.1'))
    user = models.ForeignKey(User, db_column='uid')
    admin = models.ForeignKey(Admin, db_column='aid')
    module = models.CharField(max_length=20, default="Dv")
    action_type = models.PositiveSmallIntegerField(default=3)

    class Meta:
        db_table = 'admin_actions'
        ordering = ['-datetime']


class Fees(models.Model):

    date = models.DateTimeField(default=datetime.datetime.now)
    sum = models.FloatField(default=0)
    aid = models.ForeignKey(Admin,db_column='aid')
    uid = models.ForeignKey('User', db_column='uid')
    bill = models.ForeignKey(Bill,related_name='fees')
    ip = models.IntegerField(default=ip_to_num('127.0.0.1'))
    last_deposit = models.FloatField(default=0)
    #inner_describe = models.CharField(max_length=80, db_column='dsc')
    dsc = models.CharField(max_length=80, db_column='dsc')
    method = models.ForeignKey('FeesTypes', db_column='method')

    class Meta:
        db_table = 'fees'
        ordering = ['date']

    def __unicode__(self):
        return self.sum

    def ip_to_num(self, ip_addr):
        sets = map(int, ip_addr.split("."))
        return int(sets[0]*256**3 + sets[1]*256**2 + sets[2]*256 + sets[3])

    def num_to_ip(self, number):
        d = number % 256
        c = int(number/256) % 256
        b = int(number/(256**2)) % 256
        a = int(number/(256**3)) % 256
        return "%s.%s.%s.%s" % (a, b, c, d)

    def get_ip(self):
        return self.num_to_ip(self.ip)


class FeesTypes(models.Model):
    sum = models.FloatField(db_column='sum')
    name = models.CharField(max_length=100, db_column='name')
    class Meta:
        db_table = 'fees_types'
        ordering = ['id']

class Shedule(models.Model):
    uid = models.IntegerField(db_column='uid')
    date = models.DateField(db_column='date')
    type = models.CharField(max_length=100, db_column='type')
    action = models.CharField(max_length=100, db_column='action')
    aid = models.IntegerField(db_column='aid')
    d = models.CharField(max_length=100, db_column='d')
    m = models.CharField(max_length=100, db_column='m')
    y = models.CharField(max_length=100, db_column='y')
    module = models.CharField(max_length=12, db_column='module')
    comments = models.TextField(db_column='comments')

    class Meta:
        db_table = 'shedule'
