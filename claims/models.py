from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.utils import timezone
import re
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=False,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password, True, True, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user


def avatar_upload_path(instance, filename):
        """Generates upload path for FileField"""
        return u"claims/images/%s/%s" % (instance.username, filename)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('username', max_length=30, unique=True,
                                help_text=_('Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters'),
                                validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'), 'Enter a valid username.', 'invalid')])
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    email = models.EmailField(_('email address'), max_length=255)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=False,
                                help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    receive_newsletter = models.BooleanField(_('receive newsletter'), default=False)
    claims_per_page = models.IntegerField(default=25)
    comments_per_page = models.IntegerField(default=10)
    logs_per_page = models.IntegerField(default=10)
    queue = models.ForeignKey('Queue', blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)
    # groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True,
    #                                 help_text=_('The groups this user belongs to. A user will get all permissions granted to each of his/her group.'),
    #                                 related_name="tmp_user_set", related_query_name="user")
    # user_permissions = models.ManyToManyField(Permission,
    #                                           verbose_name=_('user permissions'), blank=True,
    #                                           help_text=_('Specific permissions for this user.'),
    #                                           related_name="tmp_user_set", related_query_name="user")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def last_seen(self):
        return cache.get('seen_%s' % self.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False


class Claims(models.Model):
    address = models.CharField(max_length=500)
    uid = models.IntegerField(blank=True, null=True)
    login = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=500, blank=True, null=True)
    queue = models.ForeignKey('Queue', default=1, related_name='claims')
    owner = models.ForeignKey('User', related_name='owner')
    problem = models.CharField(max_length=1000)
    state = models.ForeignKey('ClaimState', default=1)
    priority = models.ForeignKey('Priority', default=1)
    created = models.DateTimeField(auto_now_add=True)
    closed = models.DateTimeField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    worker = models.ForeignKey('Workers', related_name='workers', blank=True, null=True)
    issued = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.address

    def get_absolute_url(self):
        return reverse('claim_edit', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.worker is not None:
            self.issued = datetime.datetime.now()
        else:
            pass
        if self.state_id == 2 and self.closed == None:
            self.closed = datetime.datetime.now()
        elif self.state_id == 1 and self.closed != None:
            self.closed = None
        super(Claims, self).save(*args, **kwargs)


class Queue(models.Model):
    name = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name


class ClaimState(models.Model):
    name = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name


class Priority(models.Model):
    name = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name


class Comments(models.Model):
    user = models.ForeignKey(User)
    claim = models.ForeignKey(Claims)
    title = models.CharField(max_length=500, default='Comment', blank=True)
    comments = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title


class Workers(models.Model):
    name = models.CharField(max_length=500, default='')
    disable = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Log(models.Model):
    user = models.ForeignKey('User')
    claim = models.ForeignKey('Claims', blank=True, null=True)
    action = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user.username