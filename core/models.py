# -*- encoding: utf-8 -*-
from django.db import models
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
    objects = BaseUserManager()
    #last_login = models.DateTimeField(blank=True, null=True, db_column='last_login')
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.id

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


    class Meta:
        db_table = 'admins'
        ordering = ['id']


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

    def __unicode__(self):
        return self.login

    class Meta:
        db_table = 'users'
        ordering = ['login']

    @property
    def bill(self):
        try:
            c = Company.objects.get(id=self.company.id)
            return Bill.objects.get(company_id=c.id)
        except Company.DoesNotExist:
            try:
                return Bill.objects.get(uid=self.id)
            except Bill.DoesNotExist:
                return None


    @property
    def pi(self):
        try:
            return UserPi.objects.get(id=self.id)
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

    name = models.CharField(max_length=120,unique=True)
    zip = models.CharField(max_length=100)
    city = models.CharField(max_length=300)

    def __unicode__(self):
        return self.name


    class Meta:
        db_table = 'districts'
        ordering = ['name']


class Street(models.Model):

    name = models.CharField(max_length=120, unique=True, default='')
    district = models.ForeignKey('District')

    def __unicode__(self):
        return self.name


    class Meta:
        db_table = 'streets'
        ordering = ['name']


class House(models.Model):

    number = models.CharField(max_length=120, blank=True, null=True, default='')

    def __unicode__(self):
        return self.number

    class Meta:
        db_table = 'builds'
        ordering = ['number']


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

    id = models.OneToOneField('User', related_name="user_pi", primary_key=True, db_column='uid', unique=True)
    fio = models.CharField(max_length=100, unique=True)
    #house = models.ForeignKey('House', max_length=100, db_column='address_build', blank=True, default='0')
    email = models.EmailField(db_column='email')
    street = models.ForeignKey('Street', max_length=100, db_column='address_street')
    kv = models.CharField(max_length=10, db_column='address_flat')
    phone = models.CharField(max_length=100, db_column='phone')
    city = models.CharField(max_length=100, db_column='city')
    location = models.ForeignKey('House', db_column='location_id', related_name='location', blank=True, default='0')

    def __unicode__(self):
        return '%s' % self.id

    class Meta:
        db_table = 'users_pi'
        ordering = ['fio']

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
    ip = models.IntegerField(max_length=120, db_column='ip')
    netmask = models.IntegerField(max_length=120, db_column='netmask')
    logins = models.IntegerField(max_length=120, db_column='logins')
    filter_id = models.CharField(max_length=120, db_column='filter_id')
    tp = models.ForeignKey(Tp)

    class Meta:
        db_table = 'dv_main'
        ordering = ['user__login']

    def __unicode__(self):
        return "%s - %s" % (self.user.login, self.tp.name)

class Dv_calls(models.Model):
    status = models.IntegerField(default=0, db_column='status')
    user_name = models.CharField(max_length=32, db_column='user_name')
    started = models.DateField(default='0000-00-00 00:00:00', db_column='started')
    nas_ip_address = models.IntegerField(default=0, db_column='nas_ip_address')
    nas_port_id = models.IntegerField(default=0, db_column='nas_port_id')
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
    nas_id = models.SmallIntegerField(default=0, db_column='nas_id')
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


class Iptv(models.Model):
    uid = models.OneToOneField(User, db_column='uid', primary_key=True)
    tp = models.ForeignKey(Tp, db_column='tp_id')
    mac = models.CharField(max_length=120, db_column='cid')
    disable = models.CharField(max_length=1, default=0, db_column='disable')
    registration = models.DateField(db_column='registration')
    serial = models.CharField(max_length=120, blank=True, db_column='pin')

    class Meta:
        db_table = 'iptv_main'
        ordering = ['-registration']

    def __unicode__(self):
        return str(self.uid)


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